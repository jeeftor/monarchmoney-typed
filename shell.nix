{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.uv
  ];

  shellHook = ''
    # Only create/sync venv if it doesn't exist
    if [ ! -d ".venv" ]; then
      uv sync --group dev
    fi
    # Activate the environment
    source .venv/bin/activate
  '';
}
