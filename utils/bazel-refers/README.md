# This project is for experimenting on Bazel

## Install bazel 

* Reference: https://bazel.build/install/ubuntu
```
 - sudo apt install apt-transport-https curl gnupg -y
 - curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
 - sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
 - echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
 - sudo apt update && sudo apt install bazel
```

## Install

* Reference : https://earthly.dev/blog/build-golang-bazel-gazelle/
```
go install github.com/bazelbuild/bazel-gazelle/cmd/gazelle@latest
``` 

## Project Layout

* Bazel-from-Scratch
* golang_bazel_example

## Refrences
* [all-round](https://github.com/johanbrandhorst/bazel-mono/tree/master)
