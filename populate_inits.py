import os

# Diretório raiz onde os pacotes estão (ex: 'domain')
# Você pode adicionar 'tests' aqui se também quiser popular os inits de lá.
# Ajuste 'START_DIR' se sua estrutura for 'src/domain'.
START_DIR = "api"


def populate_init_files(basedir):
    """
    Percorre recursivamente os diretórios a partir de 'basedir',
    encontrando todos os arquivos __init__.py.
    Para cada __init__.py, adiciona imports de todos os arquivos .py
    no mesmo diretório.
    """
    print(f"[*] Iniciando a busca em: {basedir}")

    for root, dirs, files in os.walk(basedir):
        # Ignora diretórios __pycache__
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        init_file_path = os.path.join(root, "__init__.py")

        # Garante que o arquivo __init__.py exista
        if not os.path.exists(init_file_path):
            print(f"[*] Aviso: Criando arquivo __init__.py ausente em {root}")
            open(init_file_path, "a").close()

        # Lista de módulos para importar (arquivos .py no diretório atual)
        modules_to_import = []
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                module_name = f[:-3]  # Remove o '.py'
                modules_to_import.append(module_name)

        if modules_to_import:
            print(f"[*] Populando: {init_file_path}")

            # Gera as linhas de import
            # Ex: "from .my_file import MyFile" (assumindo que o nome da classe é o
            # nome do arquivo em PascalCase)
            # Nota: Isso usa uma convenção comum. Se sua classe tiver um nome diferente,
            # você pode preferir usar "from . import module_name"

            import_lines = []
            for module in modules_to_import:
                # Converte 'my_file_name' para 'MyFileName'
                class_name = "".join(word.capitalize() for word in module.split("_"))

                # Gera a linha de import
                line = f"from .{module} import {class_name}\n"
                import_lines.append(line)

            # Escreve as linhas no arquivo __init__.py, sobrescrevendo o conteúdo
            # antigo.
            try:
                with open(init_file_path, "w") as f:
                    f.writelines(import_lines)
                print(f"    -> Sucesso. Adicionadas {len(import_lines)} importações.")
            except Exception as e:
                print(f"    -> ERRO ao escrever em {init_file_path}: {e}")


if __name__ == "__main__":
    if not os.path.isdir(START_DIR):
        print(f"Erro: O diretório '{START_DIR}' não foi encontrado.")
        print("Rode este script da raiz do seu projeto (ex: /home/devuser/app).")
    else:
        populate_init_files(START_DIR)
        print("\n[*] Concluído.")
