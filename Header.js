import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Header = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Gerenciador de Tarefas
        </Typography>
        
        {isAuthenticated ? (
          <Box>
            <Button 
              color="inherit" 
              component={RouterLink} 
              to="/tasks"
            >
              Tarefas
            </Button>
            <Button 
              color="inherit" 
              component={RouterLink} 
              to="/tasks/new"
            >
              Nova Tarefa
            </Button>
            <Button 
              color="inherit" 
              onClick={handleLogout}
            >
              Sair
            </Button>
          </Box>
        ) : (
          <Box>
            <Button 
              color="inherit" 
              component={RouterLink} 
              to="/login"
            >
              Login
            </Button>
            <Button 
              color="inherit" 
              component={RouterLink} 
              to="/register"
            >
              Registrar
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
