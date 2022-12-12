import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import InputAdornment from '@mui/material/InputAdornment';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import IconButton from '@mui/material/IconButton';
import Container from '@mui/material/Container';
import { AuthContext } from '../../utils/providers/auth';
import { clearMessage, setMessage } from '../../core/slices/message';

const LogIn = () => {
  const [values, setValues] = useState({
    amount: '',
    password: '',
    weight: '',
    weightRange: '',
    showPassword: false,
  });
  const context = useContext(AuthContext);
  const { message } = useSelector(state => state.message);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(clearMessage());
  }, []);

  const handleClickShowPassword = () => {
    setValues({
      ...values,
      showPassword: !values.showPassword,
    });
  };

  const handleFocus = el => {
    dispatch(setMessage({ ...message, [el]: '', detail: '' }));
  };

  const handleSubmit = event => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    context.login({ email: data.get('email'), password: data.get('password') });
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
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
            error={!!message?.email || !!message?.detail}
            helperText={message?.email}
            onFocus={() => handleFocus('email')}
          />
          <TextField
            sx={{ mb: 2 }}
            fullWidth
            label="Пароль"
            name="password"
            placeholder="Пароль"
            id="password"
            autoComplete="current-password"
            type={values.showPassword ? 'text' : 'password'}
            error={!!message?.password || !!message?.detail}
            helperText={message?.password}
            onFocus={() => handleFocus('password')}
            InputProps={{
              endAdornment:
                  (
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={handleClickShowPassword}
                      >
                        {values.showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
            }}
          />
          <div style={{ textAlign: 'right' }}>
            <Link to="/recovery-password" variant="body2" underline="none">
              Забыли пароль?
            </Link>
          </div>
          {message?.detail && (
            <Typography sx={{ mt: 2 }} color="error.main">{message?.detail}</Typography>
          )}
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
              <Link to="/register" variant="body2" underline="none">
                Зарегистрироваться
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};
export default LogIn;
