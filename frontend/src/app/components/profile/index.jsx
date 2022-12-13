import React, { useState } from 'react';
import { Avatar, Button } from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import background from '../../../assets/public/profile_background.jpg';
import avatar from '../../../assets/public/profile_avatar.jpg';

import './index.scoped.scss';

const Profile = () => {
  const [openText, setOpenText] = useState(true);

  return (
    <>
      <Typography
        component="h4"
        variant="h6"
        fontWeight="500"
        color="primary"
        sx={{ paddingBottom: '30px' }}
      >
        Профиль
      </Typography>
      <Card sx={{ height: '90%' }}>
        <CardMedia
          component="img"
          height="168"
          image={background}
          alt="user's background"
        />
        <CardContent>
          <Avatar
            src={avatar}
            sx={{
              width: 128, height: 128, marginTop: '-80px', marginLeft: '30px', marginBottom: '12px',
            }}
          />
          <Typography variant="iter_h1" sx={{ paddingBottom: '3px', display: 'block' }}>Иван Иванов</Typography>
          <Typography
            variant="iter_h2"
            sx={{ paddingBottom: '20px', color: '#6C757D', display: 'block' }}
          >
            @ivan
          </Typography>
          <Typography variant="iter_h2" paragraph noWrap={openText}>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
          </Typography>
          <Button
            variant="text"
            size="small"
            sx={{ textTransform: 'none', left: '90%', position: 'relative' }}
            onClick={() => setOpenText(!openText)}
          >
            {openText === true ? 'больше' : 'меньше'}
          </Button>
        </CardContent>
      </Card>
    </>
  );
};

export default Profile;
