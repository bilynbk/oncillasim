cmake_minimum_required(VERSION 2.8)

find_program(ONCILLASIM_MANUAL_SPHINX_BUILD "sphinx-build")
set(ONCILLASIM_MANUAL_SPHINX_OPTIONS ""
    CACHE STRING
    "Options to pass to the sphinx-build program.")

set(ONCILLASIM_MANUAL_RSC_MANUAL_INVENTORY_DIR ""
    CACHE STRING
    "The directory or URL containing the objects.inv file for RSC's Sphinx documentation.")
set(ONCILLASIM_MANUAL_RSB_MANUAL_INVENTORY_DIR ""
    CACHE STRING
    "The directory or URL containing the objects.inv file for RSB's Sphinx documentation.")
set(ONCILLASIM_MANUAL_RST_MANUAL_INVENTORY_DIR ""
    CACHE STRING
    "The directory or URL containing the objects.inv file for RST's Sphinx documentation.")

configure_file(Makefile.sphinx.in Makefile.sphinx @ONLY)
configure_file(conf.py.in         conf.py         @ONLY)

install(DIRECTORY _build/html
        DESTINATION "share/doc/libcca-oncilla-manual/")
