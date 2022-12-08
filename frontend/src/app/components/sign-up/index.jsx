import React, { useContext, useState } from 'react';
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
import { AuthContext } from '../../utils/providers/auth';

const SignUp = () => {
  const [values, setValues] = useState({
    amount: '',
    password: '',
    weight: '',
    weightRange: '',
    showPassword: false,
  });
  const context = useContext(AuthContext);

  const handleChange = prop => event => {
    setValues({ ...values, [prop]: event.target.value });
  };

  const handleClickShowPassword = () => {
    setValues({
      ...values,
      showPassword: !values.showPassword,
    });
  };

  const handleMouseDownPassword = event => {
    event.preventDefault();
  };

  const handleSubmit = event => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    context.register({ email: data.get('email'), password: data.get('password') });
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
          Регистрация
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
                    onMouseDown={handleMouseDownPassword}
                  >
                    {values.showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              )}
            />
          </FormControl>
          <Button
            type="submit"
            size="large"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Зарегистрироваться
          </Button>
          <Grid container spacing={1} alignItems="center" justifyContent="center">
            <Grid item>
              <Typography variant="body2">
                Уже есть аккаунт?
              </Typography>
            </Grid>
            <Grid item>
              <Link to="/login" variant="body2" underline="none">
                Войти
              </Link>
            </Grid>
          </Grid>
        </Box>
        <div style={{ position: 'absolute', bottom: 32 }}>
          <Typography variant="caption">
            Нажимая на кнопку «Зарегистрироваться», я подтверждаю,
          </Typography>
          <Grid container justifyContent="center" spacing={1}>
            <Grid item>
              <Typography variant="caption">
                что ознакомлен(а) с
              </Typography>
            </Grid>
            <Grid item>
              <Link variant="caption" underline="none">
                пользовательским соглашением
              </Link>
            </Grid>
          </Grid>
        </div>
      </Box>
    </Container>
  );
};

export default SignUp;
