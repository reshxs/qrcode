import enum
import pathlib

from typer import Argument, Typer, Option
import qrcode


cli = Typer()


class ErrorCorrectionLevel(str, enum.Enum):
    M = 'M'
    L = 'L'
    Q = 'Q'
    H = 'H'

    def as_qrcode_correction_level(self):
        if self.value == 'M':
            return qrcode.constants.ERROR_CORRECT_M
        elif self.value == 'L':
            return qrcode.constants.ERROR_CORRECT_L
        elif self.value == 'Q':
            return qrcode.constants.ERROR_CORRECT_Q
        elif self.value == 'H':
            return qrcode.constants.ERROR_CORRECT_H
        else:
            raise NotImplementedError


@cli.command(
    short_help='Сгенирировать QR-code',
)
def make(
    input_data: str = Argument(...),
    output_path: pathlib.Path = Option('qrcode.png', '--output', '-o', help='Путь до выходного файла'),
    version: int = Option(None, '--version', '-v', help='Версия QR кода'),
    errors_correction: ErrorCorrectionLevel = Option(None, '--correction', '-c', help='Уровень коррекции'),
):
    kwargs = {}

    if version is not None:
        kwargs['version'] = version

    if errors_correction is not None:
        kwargs['error_correction'] = errors_correction.as_qrcode_correction_level()

    data = qrcode.make(input_data, **kwargs)

    with open(output_path.as_posix(), 'wb') as file:
        data.save(file)


if __name__ == "__main__":
    cli()
