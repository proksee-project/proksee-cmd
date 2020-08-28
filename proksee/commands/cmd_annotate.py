import click
import os


@click.command('annotate',
               short_help='Annotate an assembly.')
@click.argument('assembly', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output_dir', required=True,
              type=click.Path(exists=False, file_okay=False, dir_okay=True, writable=True))
@click.pass_context
def cli(ctx, assembly, output_dir):

    raise click.UsageError("command not yet implemented")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
