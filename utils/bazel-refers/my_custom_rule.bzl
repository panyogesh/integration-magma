def write_new_file_impl(ctx):
    
    output_file = ctx.actions.declare_file(ctx.attr.out_file_name + ".txt")
    
    shell_command = "/bin/bash -c 'cat {} >> {}'".format(ctx.file.my_input_file.path, output_file.path)

    ctx.actions.run_shell(
        command = shell_command,
        inputs = [ctx.file.my_input_file],
        outputs = [output_file]
    )

    return DefaultInfo(files = depset([output_file]))

write_new_file  = rule(
    implementation = write_new_file_impl,
    attrs = {
        "my_input_file": attr.label(allow_single_file = True),
        "out_file_name": attr.string()
    }
)