{
  # Based on zero-to-nix Python template
  # at https://github.com/DeterminateSystems/zero-to-nix/
  description = "Development environment for the simplenet_tui project";

  # Flake inputs
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  # Flake outputs
  outputs = { self, nixpkgs }:
    let
      # Systems supported
      allSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
        "x86_64-darwin" # 64-bit Intel macOS
        "aarch64-darwin" # 64-bit ARM macOS
      ];

      # Helper to provide system-specific attributes
      nameValuePair = name: value: { inherit name value; };
      genAttrs = names: f: builtins.listToAttrs (map (n: nameValuePair n (f n)) names);
      forAllSystems = f: genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      # Development environment output
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
            # The Nix packages provided in the environment
            packages = with pkgs; [
              (python311.withPackages (ps: with ps; [
                black
                flake8
              ]))

              netcat-gnu
            ];

            # Environment variables provided in the environment
            PROJECT = "simplenet_tui";

            # Hook commands to run in the environment
            shellHook = ''
              echo
              echo $PROJECT dev environment
              echo -----------------------------
              echo
              echo use the \"simplenet\" command to run

              alias simplenet='python $PWD/src/main.py'
            '';
          };
      });
    };
}

