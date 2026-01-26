# What's Changed?

## Unrealesed

### V1.0.0
- First commit
- Added README.md and CHANGELOG.md

### V1.0.1
- Added users app in ./apps/users/
- Added views, serializers, models, signals, urls in users app
- Added register, login, logout, get and put user profile
- Using TokenAuthentication for Auth
- Added assets folder
- Minor change in config/settings and config/urls

### V1.0.2
- Added catalogues and roblox_cores apps
- Added Models to catalogues and roblox_cores apps

### V1.0.3
- Added serializers.py in apps.roblox_cores.serializers 
- Added urls.py in apps.roblox_cores.urls
- Added get, post, put, and delete in apps.roblox_cores.views
- Added apps.roblox_cores.admin for Django Admin
- Minor changes in apps.roblox_cores.models 

### V1.0.4
- Added serializers.py in apps.catalogues.serializers 
- Added urls.py in apps.catalogues.urls
- Added get, post, put, and delete in apps.catalogues.views
- Added apps.catalogues.admin for Django Admin
- Minor changes in apps.catalogues.models 

### V1.0.5
- Added serializers.py in apps.transactions.serializers 
- Added urls.py in apps.transactions.urls
- Added get, post, put, and delete in apps.transactions.views
- Added apps.transactions.admin for Django Admin
- Minor changes in apps.transactions.models 

### V1.0.6
- changed the dir from views.py to folder that contains authentications.py & profiles.py
- fixed apps.users.views & apps.users.views by using generic.views & Nested serializers

### V1.0.7
- changed endpoint in apps.users.urls

### V1.0.8
- added utils.response for JSON response structure
- fixed JSON response structure in apps.users.views 

### V1.0.9
- seperated the serializers and views classes to be related to functions that it serves  
- fixed JSON response structure in apps.transaction.views and apps.transaction.serializers 