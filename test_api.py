import unittest
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

class TestTaskManagerAPI(unittest.TestCase):
    def setUp(self):
        # Dados para teste
        self.test_user = {
            "name": "Usuário Teste",
            "email": "teste@example.com",
            "password": "senha123"
        }
        self.test_task = {
            "title": "Tarefa de Teste",
            "description": "Descrição da tarefa de teste",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": "media",
            "status": "pendente"
        }
        self.token = None
        
        # Tentar registrar o usuário (pode falhar se já existir)
        try:
            requests.post(f"{BASE_URL}/register", json=self.test_user)
        except:
            pass
        
        # Fazer login para obter o token
        login_data = {
            "username": self.test_user["email"],
            "password": self.test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/login", data=login_data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
    
    def test_01_register_user(self):
        """Teste de registro de usuário"""
        # Criar um novo usuário para teste
        test_user = {
            "name": "Novo Usuário",
            "email": f"novo{datetime.now().timestamp()}@example.com",
            "password": "senha123"
        }
        
        response = requests.post(f"{BASE_URL}/register", json=test_user)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["name"], test_user["name"])
        self.assertEqual(response.json()["email"], test_user["email"])
    
    def test_02_login(self):
        """Teste de login"""
        login_data = {
            "username": self.test_user["email"],
            "password": self.test_user["password"]
        }
        
        response = requests.post(f"{BASE_URL}/login", data=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")
    
    def test_03_create_task(self):
        """Teste de criação de tarefa"""
        if not self.token:
            self.skipTest("Token não disponível")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{BASE_URL}/tasks", json=self.test_task, headers=headers)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["title"], self.test_task["title"])
        
        # Salvar o ID da tarefa para testes posteriores
        self.task_id = response.json()["id"]
    
    def test_04_get_tasks(self):
        """Teste de listagem de tarefas"""
        if not self.token:
            self.skipTest("Token não disponível")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_05_filter_tasks(self):
        """Teste de filtragem de tarefas"""
        if not self.token:
            self.skipTest("Token não disponível")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Testar filtro por status
        response = requests.get(f"{BASE_URL}/tasks?status=pendente", headers=headers)
        self.assertEqual(response.status_code, 200)
        
        # Testar filtro por prioridade
        response = requests.get(f"{BASE_URL}/tasks?priority=media", headers=headers)
        self.assertEqual(response.status_code, 200)
        
        # Testar ordenação
        response = requests.get(f"{BASE_URL}/tasks?order_by=due_date&order_direction=asc", headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_06_update_task(self):
        """Teste de atualização de tarefa"""
        if not self.token or not hasattr(self, 'task_id'):
            self.skipTest("Token ou task_id não disponível")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        update_data = {
            "title": "Tarefa Atualizada",
            "status": "em_andamento"
        }
        
        response = requests.put(f"{BASE_URL}/tasks/{self.task_id}", json=update_data, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], update_data["title"])
        self.assertEqual(response.json()["status"], update_data["status"])
    
    def test_07_delete_task(self):
        """Teste de exclusão de tarefa"""
        if not self.token or not hasattr(self, 'task_id'):
            self.skipTest("Token ou task_id não disponível")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.delete(f"{BASE_URL}/tasks/{self.task_id}", headers=headers)
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a tarefa foi realmente excluída
        response = requests.get(f"{BASE_URL}/tasks/{self.task_id}", headers=headers)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
