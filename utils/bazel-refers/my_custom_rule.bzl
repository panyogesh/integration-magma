def write_new_file_impl(ctx):
    pass

write_new_file  = rule(
    implementation = write_new_file_impl,
)