make distclean
make ARCH=arm CROSS_COMPILE=arm-none-eabi- csk6011a-nano_defconfig
make ARCH=arm CROSS_COMPILE=arm-none-eabi-
python3 ./patch_bin.py ./u-boot-nodtb.bin
python3 ./patch_bin.py ./u-boot-dtb.bin
