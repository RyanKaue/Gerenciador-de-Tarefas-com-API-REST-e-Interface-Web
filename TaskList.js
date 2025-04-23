import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { 
  Container, 
  Paper, 
  Typography, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Button,
  IconButton,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Grid,
  Chip
} from '@mui/material';
import { Edit, Delete, Add, FilterList } from '@mui/icons-material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import ptBR from 'date-fns/locale/pt-BR';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  
  // Filtros
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [dueDateFilter, setDueDateFilter] = useState(null);
  const [orderBy, setOrderBy] = useState('due_date');
  const [orderDirection, setOrderDirection] = useState('asc');
  
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
  }, [statusFilter, priorityFilter, dueDateFilter, orderBy, orderDirection]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      
      // Construir parâmetros de consulta para filtros
      let params = new URLSearchParams();
      if (statusFilter) params.append('status', statusFilter);
      if (priorityFilter) params.append('priority', priorityFilter);
      if (dueDateFilter) params.append('due_date_before', dueDateFilter.toISOString());
      params.append('order_by', orderBy);
      params.append('order_direction', orderDirection);
      
      const response = await axios.get(`http://localhost:8000/tasks?${params.toString()}`);
      setTasks(response.data);
      setError('');
    } catch (error) {
      console.error('Erro ao buscar tarefas:', error);
      setError('Falha ao carregar tarefas. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (id) => {
    navigate(`/tasks/edit/${id}`);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
      try {
        await axios.delete(`http://localhost:8000/tasks/${id}`);
        // Atualizar a lista após exclusão
        fetchTasks();
      } catch (error) {
        console.error('Erro ao excluir tarefa:', error);
        setError('Falha ao excluir tarefa. Por favor, tente novamente.');
      }
    }
  };

  const handleAddNew = () => {
    navigate('/tasks/new');
  };

  const toggleFilters = () => {
    setShowFilters(!showFilters);
  };

  const clearFilters = () => {
    setStatusFilter('');
    setPriorityFilter('');
    setDueDateFilter(null);
    setOrderBy('due_date');
    setOrderDirection('asc');
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'alta':
        return 'error';
      case 'media':
        return 'warning';
      case 'baixa':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pendente':
        return 'warning';
      case 'em_andamento':
        return 'info';
      case 'concluida':
        return 'success';
      default:
        return 'default';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Sem data';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
  };

  return (
    <Container>
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5" component="h2">
            Minhas Tarefas
          </Typography>
          <Box>
            <Button 
              variant="outlined" 
              startIcon={<FilterList />} 
              onClick={toggleFilters}
              sx={{ mr: 1 }}
            >
              Filtros
            </Button>
            <Button 
              variant="contained" 
              startIcon={<Add />} 
              onClick={handleAddNew}
            >
              Nova Tarefa
            </Button>
          </Box>
        </Box>

        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}

        {showFilters && (
          <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Filtros e Ordenação
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    value={statusFilter}
                    label="Status"
                    onChange={(e) => setStatusFilter(e.target.value)}
                  >
                    <MenuItem value="">Todos</MenuItem>
                    <MenuItem value="pendente">Pendente</MenuItem>
                    <MenuItem value="em_andamento">Em Andamento</MenuItem>
                    <MenuItem value="concluida">Concluída</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth>
                  <InputLabel>Prioridade</InputLabel>
                  <Select
                    value={priorityFilter}
                    label="Prioridade"
                    onChange={(e) => setPriorityFilter(e.target.value)}
                  >
                    <MenuItem value="">Todas</MenuItem>
                    <MenuItem value="baixa">Baixa</MenuItem>
                    <MenuItem value="media">Média</MenuItem>
                    <MenuItem value="alta">Alta</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
                  <DatePicker
                    label="Data Limite Até"
                    value={dueDateFilter}
                    onChange={(newValue) => setDueDateFilter(newValue)}
                    renderInput={(params) => <TextField {...params} fullWidth />}
                  />
                </LocalizationProvider>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth>
                  <InputLabel>Ordenar Por</InputLabel>
                  <Select
                    value={orderBy}
                    label="Ordenar Por"
                    onChange={(e) => setOrderBy(e.target.value)}
                  >
                    <MenuItem value="due_date">Data Limite</MenuItem>
                    <MenuItem value="priority">Prioridade</MenuItem>
                    <MenuItem value="created_at">Data de Criação</MenuItem>
                    <MenuItem value="status">Status</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <FormControl>
                    <InputLabel>Direção</InputLabel>
                    <Select
                      value={orderDirection}
                      label="Direção"
                      onChange={(e) => setOrderDirection(e.target.value)}
                      sx={{ minWidth: 120 }}
                    >
                      <MenuItem value="asc">Crescente</MenuItem>
                      <MenuItem value="desc">Decrescente</MenuItem>
                    </Select>
                  </FormControl>
                  <Button variant="outlined" onClick={clearFilters}>
                    Limpar Filtros
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        )}

        {loading ? (
          <Typography>Carregando tarefas...</Typography>
        ) : tasks.length === 0 ? (
          <Typography>Nenhuma tarefa encontrada.</Typography>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Título</TableCell>
                  <TableCell>Descrição</TableCell>
                  <TableCell>Data Limite</TableCell>
                  <TableCell>Prioridade</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tasks.map((task) => (
                  <TableRow key={task.id}>
                    <TableCell>{task.title}</TableCell>
                    <TableCell>{task.description || 'Sem descrição'}</TableCell>
                    <TableCell>{formatDate(task.due_date)}</TableCell>
                    <TableCell>
                      <Chip 
                        label={task.priority.charAt(0).toUpperCase() + task.priority.slice(1)} 
                        color={getPriorityColor(task.priority)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={task.status === 'em_andamento' ? 'Em Andamento' : 
                              task.status.charAt(0).toUpperCase() + task.status.slice(1)} 
                        color={getStatusColor(task.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <IconButton 
                        color="primary" 
                        onClick={() => handleEdit(task.id)}
                        size="small"
                      >
                        <Edit />
                      </IconButton>
                      <IconButton 
                        color="error" 
                        onClick={() => handleDelete(task.id)}
                        size="small"
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Container>
  );
};

export default TaskList;
