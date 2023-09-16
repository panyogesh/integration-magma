  # Command for generating cscope and ctags for golang

  * find $go_pkg_src -name "*.go" -print > cscope.files
  * find . -name "*.go" -print >> cscope.files
  * cscope -b -k
  * ctags -R



