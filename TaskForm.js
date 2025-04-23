import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { 
  Container, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Box,
  Alert
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import ptBR from 'date-fns/locale/pt-BR';

const TaskForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = !!id;
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    due_date: null,
    priority: 'media',
    status: 'pendente'
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  useEffect(() => {
    if (isEditMode) {
      fetchTask();
    }
  }, [id]);
  
  const fetchTask = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/tasks/${id}`);
      const task = response.data;
      
      setFormData({
        title: task.title,
        description: task.description || '',
        due_date: task.due_date ? new Date(task.due_date) : null,
        priority: task.priority,
        status: task.status
      });
      
    } catch (error) {
      console.error('Erro ao buscar tarefa:', error);
      setError('Falha ao carregar dados da tarefa. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleDateChange = (date) => {
    setFormData(prev => ({
      ...prev,
      due_date: date
    }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title) {
      setError('O título é obrigatório');
      return;
    }
    
    try {
      setLoading(true);
      setError('');
      
      const dataToSend = {
        ...formData,
        due_date: formData.due_date ? formData.due_date.toISOString() : null
      };
      
      if (isEditMode) {
        await axios.put(`http://localhost:8000/tasks/${id}`, dataToSend);
        setSuccess('Tarefa atualizada com sucesso!');
      } else {
        await axios.post('http://localhost:8000/tasks', dataToSend);
        setSuccess('Tarefa criada com sucesso!');
        
        // Limpar formulário após criação
        setFormData({
          title: '',
          description: '',
          due_date: null,
          priority: 'media',
          status: 'pendente'
        });
      }
      
      // Redirecionar após um breve delay para mostrar a mensagem de sucesso
      setTimeout(() => {
        navigate('/tasks');
      }, 1500);
      
    } catch (error) {
      console.error('Erro ao salvar tarefa:', error);
      setError('Falha ao salvar tarefa. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleCancel = () => {
    navigate('/tasks');
  };
  
  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          {isEditMode ? 'Editar Tarefa' : 'Nova Tarefa'}
        </Typography>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}
        
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Título"
            name="title"
            value={formData.title}
            onChange={handleChange}
            margin="normal"
            required
          />
          
          <TextField
            fullWidth
            label="Descrição"
            name="description"
            value={formData.description}
            onChange={handleChange}
            margin="normal"
            multiline
            rows={4}
          />
          
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
            <DatePicker
              label="Data Limite"
              value={formData.due_date}
              onChange={handleDateChange}
              renderInput={(params) => (
                <TextField {...params} fullWidth margin="normal" />
              )}
            />
          </LocalizationProvider>
          
          <FormControl fullWidth margin="normal">
            <InputLabel>Prioridade</InputLabel>
            <Select
              name="priority"
              value={formData.priority}
              label="Prioridade"
              onChange={handleChange}
            >
              <MenuItem value="baixa">Baixa</MenuItem>
              <MenuItem value="media">Média</MenuItem>
              <MenuItem value="alta">Alta</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl fullWidth margin="normal">
            <InputLabel>Status</InputLabel>
            <Select
              name="status"
              value={formData.status}
              label="Status"
              onChange={handleChange}
            >
              <MenuItem value="pendente">Pendente</MenuItem>
              <MenuItem value="em_andamento">Em Andamento</MenuItem>
              <MenuItem value="concluida">Concluída</MenuItem>
            </Select>
          </FormControl>
          
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
            <Button 
              variant="outlined" 
              onClick={handleCancel}
            >
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="contained" 
              disabled={loading}
            >
              {loading ? 'Salvando...' : isEditMode ? 'Atualizar' : 'Criar'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default TaskForm;
