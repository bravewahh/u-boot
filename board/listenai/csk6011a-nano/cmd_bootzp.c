// SPDX-License-Identifier: GPL-2.0+
/*
 * Commands to deal with Synology specifics.
 *
 * Copyright (C) 2015  Phil Sutter <phil@nwl.cc>
 */

#include <common.h>
#include <command.h>
#include <env.h>

struct zimage_header {
	uint32_t stack;
	uint32_t kernel_start;
	uint32_t reserved[7];
	uint32_t magic;
	uint32_t rom_region_start;
	uint32_t end;
} __packed;

#define ZIMAGE_HEADER_MAGIC (0x016f2818)

typedef void (*bootzep_entry)(void);

static int do_bootzp(struct cmd_tbl *cmdtp, int flag, int argc,
		   char *const argv[])
{
	int ret = 0;

	if (argc < 2)
		goto usage;

	uint32_t addr = hextoul(argv[1], NULL);

	/* with a simple check */
	if (addr < 0x18101000 || addr > 0x18400000) {
		printf("address not support@0%x\n", addr);
		return 0;
	}

	struct zimage_header *zimage_hd = (struct zimage_header *)addr;

	if (zimage_hd->magic != ZIMAGE_HEADER_MAGIC) {
		printf("zimage header magic error@%x\n", addr);
		return -1;
	}

	printf("kernel stack:%x\n", zimage_hd->stack);
	printf("kernel start:%x\n", zimage_hd->kernel_start);

	((bootzep_entry)zimage_hd->kernel_start)();

	return ret;
usage:
	return CMD_RET_USAGE;
}

U_BOOT_CMD(
	bootzp, 3, 0, do_bootzp,
	"boot zimage",
	"bootzp [address],i.e., 'bootzep 18101000'\n"
	"\tThe image to be started must have zImage headers '\n"
);
