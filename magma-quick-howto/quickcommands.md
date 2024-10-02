# Quick notes for day to day tasks

## Commands for running the clang test
* [DoozyX/clang](https://github.com/DoozyX/clang-format-lint-action)
```
clang-format-lint-action/run-clang-format.py $MAGMA_ROOT/magma/lte/gateway/c --clang-format-executable clang-format-lint-action/clang-format/clang-format9 --style "{SortIncludes: false}" --style file --exclude .git --extensions 'h,hpp,c,cpp' -r -i True
```
