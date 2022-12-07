import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import InputAdornment from '@mui/material/InputAdornment';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import Container from '@mui/material/Container';
import { FormControl } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';

const LogIn = () => {
  const [values, setValues] = useState({
    amount: '',
    password: '',
    weight: '',
    weightRange: '',
    showPassword: false,
  });

  const handleChange = prop => event => {
    setValues({ ...values, [prop]: event.target.value });
  };

  const handleClickShowPassword = () => {
    setValues({
      ...values,
      showPassword: !values.showPassword,
    });
  };

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
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h4" fontWeight="500" sx={{ mb: 3 }}>
            Войти в аккаунт
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }} className="form__container">
            <TextField
              sx={{ mb: 2 }}
              margin="normal"
              fullWidth
              id="email"
              label="Электронная почта"
              placeholder="E-mail"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <FormControl variant="outlined" fullWidth>
              <InputLabel>Пароль</InputLabel>
              <OutlinedInput
                sx={{ mb: 2 }}
                fullWidth
                label="Пароль"
                name="password"
                placeholder="Пароль"
                id="password"
                autoComplete="current-password"
                type={values.showPassword ? 'text' : 'password'}
                value={values.password}
                onChange={handleChange('password')}
                endAdornment={(
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleClickShowPassword}
                    >
                      {values.showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                    )}
              />
            </FormControl>
            <div style={{ textAlign: 'right' }}>
              <Typography component={Link} variant="body2" to="/recovery-password" sx={{ textDecoration: 'none' }}>
                 Забыли пароль?
               </Typography>
            </div>
            <Button
              type="submit"
              size="large"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Войти
            </Button>
            <Grid container spacing={1} alignItems="center" justifyContent="center">
              <Grid item>
                <Typography variant="body2">
                  Ещё нет аккаунта?
                </Typography>
              </Grid>
              <Grid item>
                <Typography component={Link} variant="body2" to="/register" sx={{ textDecoration: 'none' }}>
                   Зарегистрироваться
                </Typography>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </div>
  );
};
export default LogIn;
