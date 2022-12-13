import React, { useState } from 'react';
import MenuList from '@mui/material/MenuList';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import SearchIcon from '@mui/icons-material/Search';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import SchoolIcon from '@mui/icons-material/School';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import {
  Grid,
  Box,
  Avatar,
  Badge,
  Button,
  useMediaQuery,
} from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import NotificationsNoneIcon from '@mui/icons-material/NotificationsNone';
import SettingsIcon from '@mui/icons-material/Settings';
import logo from '../../../assets/public/profile_logo.png';
import background from '../../../assets/public/profile_background.jpg';
import avatar from '../../../assets/public/profile_avatar.jpg';
import './index.scoped.scss';

const Menu = () => {
  const matches600px = useMediaQuery('(min-width:600px)');
  const matches300px = useMediaQuery('(min-width:300px)');
  const iconSize = matches300px ? 'large' : 'small';

  if (!matches600px) {
    return (
      <Grid container sx={{ width: '100vw', justifyContent: 'space-around' }}>
        <Grid item>
          <ListItemIcon>
            <SearchIcon fontSize={iconSize} className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <FavoriteBorderIcon fontSize={iconSize} className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <SchoolIcon fontSize={iconSize} className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <CalendarMonthOutlinedIcon fontSize={iconSize} className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <AccountCircleOutlinedIcon fontSize={iconSize} className="menu_img" />
          </ListItemIcon>
        </Grid>
      </Grid>
    );
  }
  return (
    <Grid container>
      <MenuList sx={{
        display: 'flex', flexDirection: 'column', paddingLeft: '15px', paddingRight: '15px',
      }}
      >
        <img src={logo} alt="atha yoga logo" className="logo_img" />
        <MenuItem>
          <ListItemIcon>
            <SearchIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Мои занятия</ListItemText>
        </MenuItem>
        <MenuItem>
          <ListItemIcon>
            <FavoriteBorderIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Избранное</ListItemText>
        </MenuItem>
        <MenuItem>
          <ListItemIcon>
            <SchoolIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Мой прогресс</ListItemText>
        </MenuItem>
        <MenuItem>
          <ListItemIcon>
            <CalendarMonthOutlinedIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Моё расписание</ListItemText>
        </MenuItem>
        <MenuItem>
          <ListItemIcon>
            <AccountCircleOutlinedIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Профиль</ListItemText>
        </MenuItem>
      </MenuList>
    </Grid>
  );
};

const Profile = ({ user }) => {
  const [openText, setOpenText] = useState(true);
  const matches600px = useMediaQuery('(min-width:600px)');
  const matches900px = useMediaQuery('(min-width:900px)');
  const matches300px = useMediaQuery('(min-width:300px)');
  const iconSize = matches300px ? 'large' : 'small';

  const bodyHeightForLg = matches600px ? '100vh' : '';
  const typograthyStyleForNameXS = matches600px ? { paddingBottom: '3px', display: 'block' } : {
    display: 'block', paddingBottom: '3px', paddingTop: '50px', textAlign: 'center', marginBottom: '0',
  };
  const typograthyStyleForNickNameXS = matches600px ? { paddingBottom: '20px', color: '#6C757D', display: 'block' } : {
    paddingBottom: '20px', color: '#6C757D', textAlign: 'center', display: 'block',
  };
  const buttonForTextLeft = matches900px ? '-90%' : matches600px ? '-82%' : '-75%';
  const backgroundStyle = matches600px ? { height: '94%' } : { height: '94%', borderRadius: 0, marginTop: '10px' };

  return (
    <Grid
      container
      direction={matches600px === true ? 'row' : 'column'}
      justifyContent="flex-start"
      alignItems="flex-start"
      spacing={2}
      sx={{ paddingTop: '20px' }}
    >
      {matches600px
        ? (
          <Grid
            item
            tablet="auto"
            desktop="auto"
            sx={{
              justifyContent: 'center', display: 'flex', borderRight: '1px solid #DCDCDC', height: '100vh',
            }}
          >
            <Menu />
          </Grid>
        )
        : ''}

      <Grid
        item
        tablet={6}
        desktop={6}
        container
        sx={{ height: bodyHeightForLg, alignContent: 'space-between' }}
      >
        <Grid
          item
          sx={{
            width: '100vw', display: 'flex', justifyContent: 'space-between',
          }}
        >
          <Typography variant="roboto_h3" color="primary" sx={{ paddingTop: '2px' }}>Профиль</Typography>
          {matches900px === false
            ? (
              <Box sx={{ width: '80px', display: 'flex', justifyContent: 'space-evenly' }}>
                <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
                  <NotificationsNoneIcon color="action" fontSize={iconSize} />
                </Badge>
                <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
                  <SettingsIcon color="action" fontSize={iconSize} />
                </Badge>
              </Box>
            )
            : ''}
        </Grid>
        <Card sx={backgroundStyle}>
          <CardMedia
            component="img"
            height="168"
            image={background}
            alt="user's background"
          />
          <CardContent>
            {matches600px
              ? (
                <Avatar
              //    alt={user.user.name}
                  src={avatar}
                  sx={{
                    width: 128, height: 128, marginTop: '-80px', marginLeft: '30px', marginBottom: '12px',
                  }}
                />
              )
              : ((
                <Avatar
              //    alt={user.user.name}
                  src={avatar}
                  sx={{
                    width: 128, height: 128, position: 'absolute', marginTop: '-80px', marginLeft: 'calc(50% - 76px)', marginBottom: '12px',
                  }}
                />
              ))}
            <Typography variant="iter_h1" sx={typograthyStyleForNameXS}>Иван Иванов</Typography>
            <Typography variant="iter_h2" sx={typograthyStyleForNickNameXS}>@ivan</Typography>
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
            <Button variant="text" size="small" sx={{ textTransform: 'none', right: buttonForTextLeft, position: 'relative' }} onClick={() => setOpenText(!openText)}>
              {openText === true ? 'больше' : 'меньше'}
            </Button>
          </CardContent>
        </Card>
      </Grid>
      {matches900px === true
        ? (
          <Grid
            item
            tablet
            desktop
            className="notifications_box"
          >
            <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
              <NotificationsNoneIcon color="action" fontSize="large" />
            </Badge>
            <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
              <SettingsIcon color="action" fontSize="large" />
            </Badge>
          </Grid>
        )
        : ''}
      {!matches600px ? <Grid item><Menu /></Grid> : ''}
    </Grid>
  );
};

export default Profile;
