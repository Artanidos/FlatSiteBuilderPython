rm -r dist/*
rm -r packages/com.vendor.product/data/*
pyinstaller main.py
mkdir packages/com.vendor.product/data/plugins
mkdir packages/com.vendor.product/data/themes
mkdir packages/com.vendor.product/data/sources
mkdir packages/com.vendor.product/data/sites
cp -r dist/main/* packages/com.vendor.product/data
cp plugins/*.py packages/com.vendor.product/data/plugins
cp -r themes/* packages/com.vendor.product/data/themes
/home/art/Qt/Tools/QtInstallerFramework/3.1/bin/binarycreator -f -c config/config.xml -p packages FlatSiteBuilder-Linux-2.0.0.Setup

