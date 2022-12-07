import React, { useState } from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';

const PasswordRecovery = () => {
  const [values, setValues] = useState({
    amount: '',
    password: '',
    weight: '',
    weightRange: '',
    showPassword: false,
  });

  const handleSubmit = event => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log({
      email: data.get('email'),
      password: data.get('password'),
    });
  };

  return (
    <div className="container-center">
      <Container component="main" maxWidth="xs">
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h4" sx={{ mb: 4 }}>
            Восстановление пароля
          </Typography>
          <Typography variant="body2" textAlign="center">
            Мы отправим вам письмо
          </Typography>
          <Typography variant="body2" textAlign="center">
            со ссылкой для восстановления пароля
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate className="form__container">
            <TextField
              sx={{ mb: 2, mt: 1 }}
              label="Электронная почта"
              margin="normal"
              fullWidth
              id="email"
              placeholder="E-mail"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <Button
              type="submit"
              size="large"
              fullWidth
              variant="contained"
              sx={{ mt: 2, mb: 1 }}
            >
              Отправить
            </Button>
          </Box>
        </Box>
      </Container>
    </div>
  );
};
export default PasswordRecovery;
