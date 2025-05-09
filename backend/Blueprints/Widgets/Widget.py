import uuid
import traceback
import sys
from flask import render_template_string
from flask import current_app
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.Blueprints.Widgets.Static import Label

class WidgetWarning(Exception):
    """Custom exception for widget errors."""
    def __init__(self, message):
        super().__init__(message)

        self.traceback = traceback.format_exc()
        self.type, self.value, self.tb = sys.exc_info()
        self.traceback = traceback.extract_tb(self.tb)
        self.formatted_traceback = traceback.format_exception(self.type, self.value, self.tb)
        self.formatted_traceback = "".join(self.formatted_traceback)
        self.formatted_traceback = self.formatted_traceback.replace("\n", "<br>")
class WidgetWarning(Warning):
    """Custom warning for widget warnings."""
    def __init__(self, message):
        super().__init__(message)
        self.traceback = traceback.format_exc()
        self.type, self.value, self.tb = sys.exc_info()
        self.traceback = traceback.extract_tb(self.tb)
        self.formatted_traceback = traceback.format_exception(self.type, self.value, self.tb)
        self.formatted_traceback = "".join(self.formatted_traceback)
        self.formatted_traceback = self.formatted_traceback.replace("\n", "<br>")

class Widget:
    """Base class for all widgets."""
    _html_tag = "div"
    _default_css_class = "widget"

    _description = "Base widget class"
    _template = "widgets/base_widget.html"
    css_class = None
    try: 
        app = current_app
    except RuntimeError:
        app = None
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.serialized_id = None
        instance.id = lambda: instance.serialized_id if instance.serialized_id else instance.__serialize_id("default_id")
        instance.name = instance.__class__.__name__
        return instance
    
    def __init__(self):
        
        self.label: 'Label' = self.label if hasattr(self, 'label') else None
        self.before: Widget = self.before if hasattr(self, 'before') else None
        self.after: Widget = self.after if hasattr(self, 'after') else None
        self.other_attributes: dict = self.other_attributes if hasattr(self, 'other_attributes') else {}
        self.class_list = []
        
        
        
        if not hasattr(self, 'inner_html'):
            self.inner_html = None
        if self.css_class:
            self.class_list.append(self.css_class)
        else: 
            self.class_list.append(self._default_css_class)
        self.children: list[Widget] = self.children if hasattr(self, 'children') else []
        try:
          
            
            try: 
                self._description = self._description
            except AttributeError as e:
                e = WidgetWarning(e)
                print(f"Error initializing widget description: {e} - \033[31m{self.__class__.__name__}\033[0m - {self.name}")
                self._description = "Base widget class"
                pass
            # Generate HTML should always be called after initializing the widget
            try: 
                self.rendered_html = self.__get_html()
                self.html = self.rendered_html
            except Exception as e:
                e = WidgetWarning(e)
                print(f"Error generating HTML for Widget (\033[31m{self.name}\033[0m): {e}")
        
                
        except TypeError as e:
            e = WidgetWarning(e)
            print(f"Error: Unable to initialize Widget (\033[31m{self.name}\033[0m): {e} - \033[31m{self.__class__.__name__}\033[0m - {self.name}")
            raise e
        try:
            self._check_attributes()
        except WidgetWarning as e:
            print(f"Error: Widget ({self.__class__.__name__}) does not have the required attributes. {e}")
            raise e
    def __call__(self):
        # This method allows the widget to be called like a function
        if hasattr(self, 'html'):
            return self.html
    def __serialize_id(self, id: str):
        # Serialize the ID to a format suitable for HTML
        
        unique_suffix = str(uuid.uuid4())[:8]  # Generate a short unique identifier
        try:

            return f"{id(' ', '_').lower()}_{unique_suffix}"
        except AttributeError as e:
            e = WidgetWarning(e)
            print(f"Error serializing ID: {e} - \033[31m{self.__class__.__name__}\033[0m - {self.name}")
            raise e
        finally:
            # Ensure the ID is a string
            self.serialized_id = f"{self.name.replace(' ', '_').lower()}_{unique_suffix}"
            return self.serialized_id
        # Replace spaces with underscores and convert to lowercase    
    
    
    def log_warning(self, message: str):
        # Log a warning message
        if self.app:
            self.app.logger.warning(message)
        else:
            print(f"Warning: {message}")
   

     
    def __get_classes(self):
        # Generate a string of CSS classes for the widget
        try: 
            classes = " ".join(self.class_list)
            return classes
        except Warning as e:
            e = WidgetWarning(e)
            print(f"Warning: Unable to generate classes (\033[32m{self.name}\033[0m): {e} - Using default class")
            return self._default_css_class
    
    def __get_html(self):
        # Generate HTML for the widget
        html = ''
        try: 
            if hasattr(self, 'before') and self.before: 
                try:
                    html += self.before.rendered_html
                except:
                    try:
                        html += self.before.__get_html()
                    except:
                        e = WidgetWarning("Unable to generate HTML for before widget")
                        html += f'<div class="error">{e} - {self.before.name}</div>'
                        
                        
                    
        except AttributeError as e:
            e = WidgetWarning(e)
            self.log_warning(f"{e}" )
            
        
        try: 
            additional_attributes = " ".join(f'{attr}="{val}"' for attr, val in self.other_attributes.items())
        except AttributeError as e:
            additional_attributes = ""
            
        if self.label:
            if self.label.inside_widget:             
                opening_tag = f'<{self._html_tag} id="{self.id()}" class="{self.__get_classes()}" {additional_attributes}>' + self.label.html
            else:
                opening_tag = self.label.html + f'<{self._html_tag} id="{self.id()}" class="{self.__get_classes()}" {additional_attributes}>'
        else:
            opening_tag = f'<{self._html_tag} id="{self.id()}" class="{self.__get_classes()}" {additional_attributes}>'
        closing_tag = f'</{self._html_tag}>'
        
                
        html += opening_tag
        if hasattr(self, 'inner_html') and self.inner_html:
            html += self.inner_html
        
        if self.children:
            for child in self.children:
                try: 
                    if hasattr(child, 'rendered_html'):
                        html += child.rendered_html
                    else:
                        # If the child does not have rendered_html, call its __get_html method
                        child.rendered_html = child.__get_html()
                        html += child.rendered_html
                    
        
                except AttributeError as e:
                    e = WidgetWarning(e)
                    print(f"Error: Unable to generate HTML for child widget (\033[31m{child.name}\033[0m): {e} - \033[31m{self.__class__.__name__}\033[0m - {self.name}")
                    raise e
        html += f'{closing_tag}'
        if self.after: 
            html += self.after.rendered_html
        return html
    def _check_attributes(self):
        # Check if the widget has the required attributes
        if not hasattr(self, 'id'):
            raise WidgetWarning("Widget must have an ID.")
        if not hasattr(self, 'name'):
            raise WidgetWarning("Widget must have a name.")
        if not hasattr(self, '_html_tag'):
            raise WidgetWarning("Widget must have an HTML tag.")
        if not hasattr(self, 'css_class'):
            raise WidgetWarning("Widget must have a CSS class.")
        if self._description == Widget._description:
                raise WidgetWarning(f"Widget {self.name} must have a unique description.")
        
    def to_string(self):
        # Convert the widget to a string representation
        return self.html if hasattr(self, 'html') else f"{self.name} widget"

    def to_dict(self):
        # Convert the widget to a dictionary representation
        return {
            'id': self.id,
            'name': self.name,
            'html': self.html,
            'description': self._description,
            'css_class': self.__get_classes(),
            'children': [child.to_dict() for child in self.children]
        }
    
    

    
    