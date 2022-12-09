import * as React from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import logInBlockedImg from '../../../assets/public/log-in-blocked.svg';
import './style.scoped.css';

const LogInBlocked = () => (
  <div className="log_in_blocked__container">
    <div className="log_in_blocked__container-frame">
      <img src={logInBlockedImg} alt="lotus pose" />
      <Typography variant="h6" textAlign="center" sx={{mt: 5, mb: 2}}>
        Доступ к аккаунту временно заблокирован
      </Typography>
      <Typography variant="body2" color="text.secondary" maxWidth={300} textAlign="center" gutterBottom>
        Вы ввели неверный логин и/или пароль более 10 раз
      </Typography>
      <Typography variant="body2" color="text.secondary" maxWidth={250} textAlign="center">
        Вы можете обратиться за помощью в службу поддержки
        <Link href="#" variant="body2" underline="none" marginLeft={1}>
          supportEmail.
        </Link>
      </Typography>
    </div>
  </div>
);
export default LogInBlocked;
