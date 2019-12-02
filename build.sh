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
/home/art/Qt/Tools/QtInstallerFramework/3.1/bin/binarycreator -f -c config/config.xml -p packages FlatSiteBuilder-Linux-2.1.0.Setup

