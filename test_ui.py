import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class TestTaskManagerUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar o Chrome em modo headless para testes
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:3000"
        
        # Dados para teste
        cls.test_user = {
            "name": "Usuário UI Teste",
            "email": f"ui_teste_{int(time.time())}@example.com",
            "password": "senha123"
        }
        
        cls.test_task = {
            "title": "Tarefa UI Teste",
            "description": "Descrição da tarefa de teste UI",
            "priority": "alta",
            "status": "pendente"
        }
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
    def test_01_register(self):
        """Teste de registro de usuário pela UI"""
        self.driver.get(f"{self.base_url}/register")
        
        # Preencher formulário de registro
        self.driver.find_element(By.ID, "name").send_keys(self.test_user["name"])
        self.driver.find_element(By.ID, "email").send_keys(self.test_user["email"])
        self.driver.find_element(By.ID, "password").send_keys(self.test_user["password"])
        self.driver.find_element(By.ID, "confirmPassword").send_keys(self.test_user["password"])
        
        # Enviar formulário
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verificar se foi redirecionado para a página de login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login")
        )
        
        self.assertIn("/login", self.driver.current_url)
    
    def test_02_login(self):
        """Teste de login pela UI"""
        self.driver.get(f"{self.base_url}/login")
        
        # Preencher formulário de login
        self.driver.find_element(By.ID, "email").send_keys(self.test_user["email"])
        self.driver.find_element(By.ID, "password").send_keys(self.test_user["password"])
        
        # Enviar formulário
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verificar se foi redirecionado para a página de tarefas
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/tasks")
        )
        
        self.assertIn("/tasks", self.driver.current_url)
    
    def test_03_create_task(self):
        """Teste de criação de tarefa pela UI"""
        # Garantir que estamos logados
        if "/tasks" not in self.driver.current_url:
            self.test_02_login()
        
        # Navegar para a página de nova tarefa
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Nova Tarefa')]").click()
        
        # Verificar se está na página de criação de tarefa
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/tasks/new")
        )
        
        # Preencher formulário de tarefa
        self.driver.find_element(By.NAME, "title").send_keys(self.test_task["title"])
        self.driver.find_element(By.NAME, "description").send_keys(self.test_task["description"])
        
        # Selecionar prioridade
        self.driver.find_element(By.XPATH, "//div[@id='priority']").click()
        self.driver.find_element(By.XPATH, f"//li[contains(text(), 'Alta')]").click()
        
        # Enviar formulário
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verificar se foi redirecionado para a página de tarefas
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/tasks")
        )
        
        # Verificar se a tarefa foi criada
        self.assertTrue(
            self.driver.find_element(By.XPATH, f"//td[contains(text(), '{self.test_task['title']}')]").is_displayed()
        )
    
    def test_04_filter_tasks(self):
        """Teste de filtragem de tarefas pela UI"""
        # Garantir que estamos na página de tarefas
        if "/tasks" not in self.driver.current_url:
            self.driver.get(f"{self.base_url}/tasks")
        
        # Abrir filtros
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Filtros')]").click()
        
        # Selecionar filtro de prioridade
        self.driver.find_element(By.XPATH, "//div[@id='priority']").click()
        self.driver.find_element(By.XPATH, "//li[contains(text(), 'Alta')]").click()
        
        # Verificar se a tarefa criada anteriormente está visível
        self.assertTrue(
            self.driver.find_element(By.XPATH, f"//td[contains(text(), '{self.test_task['title']}')]").is_displayed()
        )
    
    def test_05_update_task(self):
        """Teste de atualização de tarefa pela UI"""
        # Garantir que estamos na página de tarefas
        if "/tasks" not in self.driver.current_url:
            self.driver.get(f"{self.base_url}/tasks")
        
        # Clicar no botão de edição da tarefa
        self.driver.find_element(By.XPATH, f"//td[contains(text(), '{self.test_task['title']}')]/following-sibling::td//button[@aria-label='edit']").click()
        
        # Verificar se está na página de edição
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/tasks/edit/")
        )
        
        # Atualizar título
        title_field = self.driver.find_element(By.NAME, "title")
        title_field.clear()
        title_field.send_keys(f"{self.test_task['title']} Atualizada")
        
        # Atualizar status
        self.driver.find_element(By.XPATH, "//div[@id='status']").click()
        self.driver.find_element(By.XPATH, "//li[contains(text(), 'Em Andamento')]").click()
        
        # Enviar formulário
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verificar se foi redirecionado para a página de tarefas
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/tasks")
        )
        
        # Verificar se a tarefa foi atualizada
        self.assertTrue(
            self.driver.find_element(By.XPATH, f"//td[contains(text(), '{self.test_task['title']} Atualizada')]").is_displayed()
        )
    
    def test_06_delete_task(self):
        """Teste de exclusão de tarefa pela UI"""
        # Garantir que estamos na página de tarefas
        if "/tasks" not in self.driver.current_url:
            self.driver.get(f"{self.base_url}/tasks")
        
        # Clicar no botão de exclusão da tarefa
        self.driver.find_element(By.XPATH, f"//td[contains(text(), '{self.test_task['title']} Atualizada')]/following-sibling::td//button[@aria-label='delete']").click()
        
        # Aceitar o alerta de confirmação
        self.driver.switch_to.alert.accept()
        
        # Esperar um pouco para a exclusão ser processada
        time.sleep(2)
        
        # Verificar se a tarefa foi removida
        task_elements = self.driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.test_task['title']} Atualizada')]")
        self.assertEqual(len(task_elements), 0)
    
    def test_07_logout(self):
        """Teste de logout pela UI"""
        # Garantir que estamos na página de tarefas
        if "/tasks" not in self.driver.current_url:
            self.driver.get(f"{self.base_url}/tasks")
        
        # Clicar no botão de logout
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sair')]").click()
        
        # Verificar se foi redirecionado para a página de login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login")
        )
        
        self.assertIn("/login", self.driver.current_url)

if __name__ == "__main__":
    unittest.main()
