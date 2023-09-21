**Console Email Backend**
- Edit the settings.py module and add the EMAIL_BACKEND variable to the end of the file:
***myproject/settings.py***

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Protecting Views Middleware**
```python
from django.contrib.auth.decorators import login_required
#USES Annotation:  @login_required
```

**Class base view**
1. Function-Based Views (FBV)
2. Class-Based Views (CBV)
3. Generic Class-Based Views (GCBV)

- A FBV is simplest representation of a Django view : it's just a function that receives an HttpRequest object
and returns an HttpResponse 

- A CBV is every Django view defined as a Python class that extends the "django.views.generic.View" abstract class.
A CBV esentilly is a class that wraps a FBV .

- When GCBV can decorate the class directly with the @login_required decorator 
```python
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
@method_decorator(login_required, name='dispatch')
#It CBV it's common to decorate the dispatch method
```


**Adding Markdown**
```bash
pip install markdown
```

1. We can add a new method to the Post model:
models.py

```python
from markdown import markdown

```