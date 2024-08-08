[app]
title = Chromatic Scale Generator
package.name = chromgen
package.domain = com.jowe
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,praat-parselmouth
orientation = portrait

# (str) Icon of the application
icon.filename = %(source.dir)s/logo.png

# Android-specific settings
fullscreen = 0
android.permissions = android.permission.READ_EXTERNAL_STORAGE, android.permission.WRITE_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
