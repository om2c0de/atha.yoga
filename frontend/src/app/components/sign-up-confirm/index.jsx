import * as React from 'react';
import { Link } from 'react-router-dom';
import Typography from '@mui/material/Typography';
import letter from '../../../assets/public/letter.svg';
import './style.scoped.css';

const SignInConfirm = () => (
  <div className="sign_in_confirm__container">
    <img src={letter} alt="Письмо" />
    <Typography variant="h6" maxWidth={270} textAlign="center" sx={{ mt: 4, mb: 2 }}>
      Письмо с подтверждением регистрации отправлено
      вам на почту
    </Typography>
    <Typography variant="body2" color="text.secondary" maxWidth={240} textAlign="center">
      Следуйте инструкции в письме.
    </Typography>
    <Typography variant="h6" maxWidth={270} textAlign="center" sx={{ mt: 4, mb: 2 }}>
      Для изменения данных вы можете вернуться к
    </Typography>
    <Typography component={Link} to="/register" variant="body2" sx={{ textDecoration: 'none' }}>
      Регистрации
    </Typography>
    <div style={{
      position: 'absolute',
      bottom: 32,
      textAlign: 'center',
      maxWidth: 380,
      lineHeight: 0.1,
    }}
    >
      <Typography variant="caption">
        Обратиться за помощью в службу поддержки
        <Typography
          component={Link}
          variant="caption"
          to="#"
          sx={{ textDecoration: 'none' }}
          marginLeft={1}
        >
          supportEmail
        </Typography>
      </Typography>
    </div>
  </div>

);
export default SignInConfirm;
