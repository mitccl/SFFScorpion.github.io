import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'Scorpion Wizard'
EXCLUDES       = [ADDON_ID, 'repository.scorpion']
# Text File with build info in it.
BUILDFILE      = 'https://sffscorpion.000webhostapp.com/vault/docs/builds.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'http://'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = ''
YOUTUBEFILE    = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONMAINT      = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONSPEED      = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONAPK        = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONADDONS     = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONYOUTUBE    = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONSAVE       = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONTRAKT      = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONREAL       = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONLOGIN      = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONCONTACT    = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
ICONSETTINGS   = 'http://sffscorpion.000webhostapp.com/vault/images/icon.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '____'

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'white'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B]([COLOR '+COLOR2+']Scorpion[/COLOR])[/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'Yes'
# You can add \n to do line breaks
CONTACT        = ''
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://'
CONTACTFANART  = 'http://'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# Url to wizard version
WIZARDFILE     = 'http://'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.scorpion'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://sffscorpion.github.io/repo/repository.scorpion/addon.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://sffscorpion.github.io/repo/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'No'
# Url to notification file
NOTIFICATION   = 'http://'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = ''
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = 'http://'
#########################################################
