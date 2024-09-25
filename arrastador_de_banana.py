import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder():
    """Abre um diálogo para selecionar uma pasta e retorna o caminho da pasta selecionada."""
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    folder = filedialog.askdirectory(title="Selecione uma pasta")
    return folder

def get_backup_category(nome_pasta):
    """Determina a categoria de backup com base no nome da pasta."""
    categorias = {
        "_MOV": "MOVELEIROS",
        "_DEC": "DECORATE"
    }
    
    for key, value in categorias.items():
        if key in nome_pasta:
            return value
    
    return "SEMCATEGORIA"

def copy_with_progress(src, dst):
    """Copia arquivos de src para dst e exibe uma barra de progresso."""
    total_files = sum([len(files) for r, d, files in os.walk(src)])
    copied_files = 0
    
    for dirpath, dirnames, filenames in os.walk(src):
        relative_path = os.path.relpath(dirpath, src)
        destination_path = os.path.join(dst, relative_path)
        os.makedirs(destination_path, exist_ok=True)

        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            shutil.copy2(source_file, destination_path)
            copied_files += 1
            
            progress = (copied_files / total_files) * 100
            bar_length = 40  # Tamanho da barra de progresso
            filled_length = int(bar_length * copied_files // total_files)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            print(f'\r|{bar}| {progress:.2f}% ({copied_files}/{total_files})', end='')

    print()  # Pula para a próxima linha após a conclusão

def prepare_destination_giben(nome_pasta, folder, furacao_path):
    """Prepara o destino para os arquivos da pasta 'giben' e executa a cópia, se disponível."""
    source_giben = os.path.join(folder, "giben")
    destination_giben = os.path.join(furacao_path, nome_pasta, "giben")
    os.makedirs(os.path.dirname(destination_giben), exist_ok=True)

    if os.path.exists(source_giben):
        print(f"Copiando arquivos de furação...")
        copy_with_progress(source_giben, destination_giben)
    else:
        print(f"A pasta \"giben\" não foi encontrada em \"{folder}\".")

def prepare_destination_img(nome_pasta, img_path, etiqueta_path):
    """Prepara o destino para as imagens e executa a cópia, se disponível."""
    source_img = os.path.join(img_path, nome_pasta)
    destination_etiqueta = os.path.join(etiqueta_path, nome_pasta)
    os.makedirs(destination_etiqueta, exist_ok=True)

    if os.path.exists(source_img):
        print(f"Copiando Etiquetas...")
        copy_with_progress(source_img, destination_etiqueta)
    else:
        print(f"A pasta ETIQUETA LOCAL não foi encontrada.")

def backup_folder(folder, nome_pasta, backup_path, categoria):
    """Realiza o backup da pasta selecionada para o local apropriado."""
    final_backup_path = os.path.join(backup_path, categoria, nome_pasta)
    os.makedirs(final_backup_path, exist_ok=True)
    copy_with_progress(folder, final_backup_path)
    print("Backup Completo!")

def main():
    backup_path = r'Z:\PROJETOS PROMOB\PROMOB PROJJE\OMAR'
    furacao_path = r'X:\FURAÇÃO PROMOB'
    img_path = r'C:\Giben\GvisionXPPROMOB\CNC\Media\Img'
    etiqueta_path = r'X:\ETIQUETA GVISION GPLAN PROMOB'

    folder = select_folder()
    if not folder:
        messagebox.showwarning("Aviso", "Nenhuma pasta selecionada.")
        return

    nome_pasta = os.path.basename(folder)
    print(f"Nome da pasta: {nome_pasta}")

    categoria = get_backup_category(nome_pasta)

    prepare_destination_giben(nome_pasta, folder, furacao_path)
    prepare_destination_img(nome_pasta, img_path, etiqueta_path)
    
    print(f"Iniciando Backup... {categoria}")
    backup_folder(folder, nome_pasta, backup_path, categoria)

if __name__ == "__main__":
    main()
