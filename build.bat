rem this only works on Windows
rem adjust the path for binarycreator
rem change version number for executable in this file
rem change the version in config/config.xml
rem change the ReleaseDate in packages/.../meta/package.xml 


pyside6-rcc main.qrc -o main_rc.py
pyside6-rcc resources.qrc -o resources.py

@REM C:\Qt\6.4.2\mingw_64\bin\lrelease translation\FlatSiteBuilder_de.ts

@REM rmdir dist\main /s /q
@REM rmdir packages\at.crowdware.FlatSiteBuilder\data /s /q

@REM pyinstaller -w main.py
@REM mkdir packages\at.crowdware.FlatSiteBuilder\data
@REM mkdir packages\at.crowdware.FlatSiteBuilder\data\plugins
@REM mkdir packages\at.crowdware.FlatSiteBuilder\data\themes
@REM mkdir packages\at.crowdware.FlatSiteBuilder\data\sources
@REM mkdir packages\at.crowdware.FlatSiteBuilder\data\translation
@REM mkdir packages\at.crowdware.FlatSiteBuilder\data\icon
@REM xcopy dist\main\*.* packages\at.crowdware.FlatSiteBuilder\data /E /H /Y
@REM xcopy plugins\*.py packages\at.crowdware.FlatSiteBuilder\data\plugins /E /H /Y
@REM xcopy themes\*.* packages\at.crowdware.FlatSiteBuilder\data\themes /E /H /Y
@REM copy translation\FlatSiteBuilder_de.qm packages\at.crowdware.FlatSiteBuilder\data\translation
@REM copy images\icon_128.ico packages\at.crowdware.FlatSiteBuilder\data\icon
@REM copy images\icon_128.png packages\at.crowdware.FlatSiteBuilder\data\icon


@REM move packages\at.crowdware.FlatSiteBuilder\data\main.exe packages\at.crowdware.FlatSiteBuilder\data\FlatSiteBuilder.exe
@REM C:\Qt\Tools\QtInstallerFramework\3.2.2\bin\binarycreator -f -c config/config.xml -p packages FlatSiteBuilder-Windows-2.3.0.Setup