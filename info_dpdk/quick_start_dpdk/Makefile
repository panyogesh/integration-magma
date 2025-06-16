# DPDK IPC Makefile

# DPDK installation path (adjust if needed)
RTE_SDK ?= $(shell pwd)/dpdk-22.11
RTE_TARGET ?= build

# Application names
PRIMARY_APP = primary_process
SECONDARY_APP = secondary_process

# Source files
PRIMARY_SRC = primary_process.c
SECONDARY_SRC = secondary_process.c

# DPDK flags
PKGCONF = pkg-config --define-prefix
PC_FILE := $(shell $(PKGCONF) --path libdpdk 2>/dev/null)

# If pkg-config is not available, use manual paths
ifeq ($(PC_FILE),)
    CFLAGS += -I$(RTE_SDK)/$(RTE_TARGET)/include
    LDFLAGS += -L$(RTE_SDK)/$(RTE_TARGET)/lib
    LDLIBS += -ldpdk -lnuma -ldl -pthread -lm
else
    CFLAGS += $(shell $(PKGCONF) --cflags libdpdk)
    LDFLAGS += $(shell $(PKGCONF) --libs libdpdk)
endif

# Compiler flags
CFLAGS += -O3 -g -W -Wall -Wextra -Wno-unused-parameter
CFLAGS += -Wno-unused-function -Wno-unused-variable

# Build rules
all: $(PRIMARY_APP) $(SECONDARY_APP)

$(PRIMARY_APP): $(PRIMARY_SRC)
        $(CC) $(CFLAGS) $< -o $@ $(LDFLAGS) $(LDLIBS)

$(SECONDARY_APP): $(SECONDARY_SRC)
        $(CC) $(CFLAGS) $< -o $@ $(LDFLAGS) $(LDLIBS)

clean:
        rm -f $(PRIMARY_APP) $(SECONDARY_APP)

install: all
        sudo cp $(PRIMARY_APP) /usr/local/bin/
        sudo cp $(SECONDARY_APP) /usr/local/bin/

.PHONY: all clean install
