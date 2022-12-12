import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import WelcomePage from './pages/welcome';
import LoginPage from './pages/auth/login';
import RegisterPage from './pages/auth/register';
import ProfilePage from './pages/profile';
import ErrorPage from './pages/error';
import PasswordRecoveryPage from './pages/password-recovery';
import AuthProvider from './utils/providers/auth';
import BaseLayout from './layouts';
import ProfileLayout from './layouts/profile';
import useAuth from './utils/hooks/useAuth';
import Calendar from './components/calendar';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import './theme/style.scss';

const theme = createTheme({
  palette: {
    primary: {
      main: '#0D6EFD',
    },
    text: {
      primary: '#212121',
      secondary: '#616161',
    },
  },
  typography: {
    h4: {
      fontWeight: 500,
    },
    h1: {
      fontWeight: 500,
    },
    h6: {
      fontSize: '1.25rem',
      lineHeight: 1.2,
    },
  },
});

const App = () => {
  const auth = useAuth();
  const Layout = auth.isLoggedIn ? ProfileLayout : BaseLayout;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/" element={<Layout auth={auth} />}>
          <Route index element={!auth.isLoggedIn ? <WelcomePage /> : <Navigate replace to="profile" />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
          <Route path="profile" element={<ProfilePage auth={auth} />} />
          <Route path="recovery-password" element={<PasswordRecoveryPage />} />
          <Route path="*" element={<ErrorPage />} />
          <Route path="calendar" element={<Calendar />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
};

const Root = () => (
  <AuthProvider>
    <App />
  </AuthProvider>
);

export default Root;
