pyrcc5 main.qrc -o main_rc.py
pyrcc5 resources.qrc -o resources.py
pyrcc5 plugins/carousel.qrc -o plugins/carousel_rc.py
pyrcc5 plugins/imageeditor.qrc -o plugins/imageeditor_rc.py
pyrcc5 plugins/revolution.qrc -o plugins/revolution_rc.py
pyrcc5 plugins/texteditor.qrc -o plugins/texteditor_rc.py
pyrcc5 plugins/github.qrc -o plugins/github_rc.py

rm -r dist/*
rm -r packages/com.vendor.product/data/*
pyinstaller main.py
#mkdir packages/com.vendor.product/data
mkdir packages/com.vendor.product/data/plugins
mkdir packages/com.vendor.product/data/themes
mkdir packages/com.vendor.product/data/sources
cp -r dist/main/* packages/com.vendor.product/data
cp plugins/*.py packages/com.vendor.product/data/plugins
cp -r themes/* packages/com.vendor.product/data/themes
mv packages/com.vendor.product/data/main packages/com.vendor.product/data/FlatSiteBuilder
/home/art/Qt/Tools/QtInstallerFramework/3.1/bin/binarycreator -f -c config/config.xml -p packages FlatSiteBuilder-Linux-2.1.2.Setup

