from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Função para coletar os produtos da página atual
def coletar_produtos(driver):
    produtos = []
    # Encontrar os elementos de título dos produtos
    resultados = driver.find_elements(By.CSS_SELECTOR, "h2.ui-search-item__title")

    # Limitar a coleta para os 3 primeiros produtos
    for i, resultado in enumerate(resultados):
        if i < 3:
            produtos.append(resultado.text)
        else:
            break  # Parar após coletar 3 produtos

    # Exibir mensagem indicando que 3 produtos foram salvos
    if produtos:
        print("Salvando 3 primeiros produtos da página.")
    else:
        print("Nenhum produto encontrado nesta página.")

    return produtos


# Função para navegar para a próxima página
def ir_para_proxima_pagina(driver):
    try:
        proxima_pagina = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@title, 'Seguinte')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", proxima_pagina)
        proxima_pagina.click()
        time.sleep(2)  # Aguardar o carregamento da página
    except Exception as e:
        print(f"Erro ao tentar ir para a próxima página: {str(e)}")
        return False
    return True


# Função para aplicar o filtro
def aplicar_filtro(driver, filtro_texto):
    try:
        # Abrir o dropdown de filtros
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.andes-dropdown__trigger"))
        )
        dropdown_button.click()

        # Esperar pelo dropdown com as opções e clicar no filtro correto
        filtro_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{filtro_texto}']/ancestor::li"))
        )
        filtro_option.click()
        time.sleep(3)  # Tempo para a página recarregar com o novo filtro
        print(f"Filtro '{filtro_texto}' aplicado.")
    except Exception as e:
        print(f"Erro ao aplicar filtro '{filtro_texto}': {str(e)}")


# Função principal para executar o scraping
def coletar_dados_mercado_livre():
    # Inicializar o navegador (Chrome)
    driver = webdriver.Chrome()
    driver.get("https://www.mercadolivre.com.br/")
    driver.maximize_window()

    # Realizar uma busca por notebooks
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "as_word"))
    )
    search_box.send_keys("notebook")
    search_box.submit()

    time.sleep(5)  # Espera para os resultados carregarem

    # Lista para armazenar todos os produtos coletados
    todos_produtos = []

    # Coletar dados sem mudar o filtro (padrão "Mais Relevantes")
    print("Coletando dados com o filtro padrão 'Mais Relevantes'...")
    for pagina in range(3):  # Limitar a coleta às 3 primeiras páginas
        print(f"Coletando dados da página {pagina + 1}...")
        produtos = coletar_produtos(driver)
        todos_produtos.extend(produtos)

        # Tentar ir para a próxima página
        if not ir_para_proxima_pagina(driver):
            break

    # Aplicar outros filtros
    filtros = ["Menor preço", "Maior preço"]

    for filtro in filtros:
        print(f"\nAplicando filtro: {filtro}")
        aplicar_filtro(driver, filtro)
        time.sleep(5)
        # Coletar dados das 3 primeiras páginas após aplicar o filtro
        for pagina in range(3):
            print(f"Coletando dados da página {pagina + 1} com o filtro '{filtro}'...")
            produtos = coletar_produtos(driver)
            todos_produtos.extend(produtos)

            # Tentar ir para a próxima página
            if not ir_para_proxima_pagina(driver):
                break

    # Fechar o navegador
    driver.quit()

    # Salvar os resultados em um arquivo de texto
    with open("produtos_coletados.txt", "w", encoding="utf-8") as f:
        for produto in todos_produtos:
            f.write(produto + "\n")

    print("\nDados salvos em 'produtos_coletados.txt'.")


# Executar o script
if __name__ == "__main__":
    coletar_dados_mercado_livre()
