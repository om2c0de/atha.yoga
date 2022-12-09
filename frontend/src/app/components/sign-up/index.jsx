import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import FormControl, { useFormControl } from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';
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
import InputLabel from '@mui/material/InputLabel';
import registerSlice from '../../core/slices/auth/register';
import { clearMessage } from '../../core/slices/message/index';
import SignUpConfirm from '../sign-up-confirm/index.jsx';
import './style.scoped.css';

const SignUp = () => {
  const [successful, setSuccessful] = useState(false);

  const { message } = useSelector(state => state.message);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(clearMessage());
  }, [dispatch]);

  const [values, setValues] = useState({
    email: '',
    amount: '',
    password: '',
    weight: '',
    weightRange: '',
    showPassword: false,
  });

  const MyFormHelperText = () => {
    const { focused } = useFormControl() || {};

    const helperText = React.useMemo(() => {
      if (focused) {
        return 'Не меньше 10 символов, знаки 3 из 4 категорий: 0-9, a-z, A-Z и специальные символы';
      }
      return '';
    }, [focused]);

    return <FormHelperText>{helperText}</FormHelperText>;
  };

  const [errorMessage, setErrorMessage] = React.useState('');

  React.useEffect(() => {
    if (values.email.length === 0) {
      setErrorMessage(
        'Заполните поле',
      );
    }
  }, [values.email]);

  React.useEffect(() => {
    if (values.email.length > 0 && errorMessage) {
      setErrorMessage('');
    }
  }, [values.email, errorMessage]);

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
    console.log({
      email: data.get('email'),
      password: data.get('password'),
    });
    const { email, password } = {
      email: data.get('email'),
      password: data.get('password'),
    };

    setSuccessful(false);

    dispatch(registerSlice({ email, password }))
      .unwrap()
      .then(() => {
        setSuccessful(true);
      })
      .catch(() => {
        setSuccessful(false);
      });
  };
  if (!successful) {
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
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }} className="form__container">
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
              error={values.email.length === 0}
              helperText={errorMessage}
              value={values.email}
            />
            <FormControl fullWidth variant="outlined" sx={{ mb: 2 }}>
              <InputLabel>Пароль</InputLabel>
              <OutlinedInput
                fullWidth
                name="password"
                label="Пароль"
                placeholder="Пароль"
                id="password"
                autoComplete="current-password"
                type={values.showPassword ? 'text' : 'password'}
                value={values.password}
                onChange={handleChange('password')}
                InputProps={{
                  endAdornment:
  <InputAdornment position="end">
    <IconButton
      aria-label="toggle password visibility"
      onClick={handleClickShowPassword}
      onMouseDown={handleMouseDownPassword}
    >
      {values.showPassword ? <VisibilityOff /> : <Visibility />}
    </IconButton>
  </InputAdornment>,
                }}
              />
              <MyFormHelperText />
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
                <Typography
                  component={Link}
                  to="/login"
                  variant="body2"
                  sx={{ textDecoration: 'none' }}
                >
                  Войти
                </Typography>
              </Grid>
            </Grid>
          </Box>
          <div style={{
            position: 'absolute',
            bottom: 32,
            textAlign: 'center',
            maxWidth: 380,
            lineHeight: 0.1,
          }}
          >
            <Typography variant="caption">
              Нажимая на кнопку «Зарегистрироваться», вы принимаете условия
              <Typography
                component={Link}
                variant="caption"
                to="#"
                sx={{ textDecoration: 'none' }}
                marginLeft={1}
              >
                Пользовательского соглашения
              </Typography>
            </Typography>
            <Typography variant="caption" sx={{ maxWidth: 300 }} marginLeft={1}>
              и
              <Typography
                component={Link}
                variant="caption"
                to="#"
                sx={{ textDecoration: 'none' }}
                marginLeft={1}
              >
                Политики конфиденциальности
              </Typography>
            </Typography>
          </div>
        </Box>
      </Container>
    );
  }
  return <SignUpConfirm />;
};

export default SignUp;
