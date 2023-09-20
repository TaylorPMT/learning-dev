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

**Accessing the Authenticated User**
```python

```