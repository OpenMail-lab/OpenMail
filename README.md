# OpenMail

A multi-service email application with microservices architecture.

## Installation

1. Download `OpenMailInstaller.exe` from the [Releases](https://github.com/OpenMail-lab/OpenMail/releases) page.
2. Run the installer to set up OpenMail.
3. Access services via the configured public IP (NAT-enabled).

## Development

- Push changes to the `main` branch to trigger CI/CD.
- Use GitHub Actions for automated builds.

## Services

- `home_service.py`: Main application service.
- `smtp_service.py`: Email sending service.