import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MobileStepper from '@mui/material/MobileStepper';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import SwipeableViews from 'react-swipeable-views';
import { autoPlay } from 'react-swipeable-views-utils';
import splash1 from '../../../assets/public/splash1.svg';
import splash2 from '../../../assets/public/splash2.svg';
import splash3 from '../../../assets/public/splash3.svg';

const AutoPlaySwipeableViews = autoPlay(SwipeableViews);

const items = [
  {
    name: 'Исследуйте',
    description: 'множество занятий и материалов \nпо различным темам и направлениям',
    image: splash1,
  },
  {
    name: 'Занимайтесь',
    description: 'в подходящее время, в удобном месте, \nс лучшими преподавателями',
    image: splash2,
  },
  {
    name: 'Создавайте',
    description: 'собственные курсы и занятия',
    image: splash3,
  },
];

const SplashScreens = () => {
  const theme = useTheme();
  const [activeStep, setActiveStep] = useState(0);
  const maxSteps = items.length;

  const handleStepChange = step => {
    setActiveStep(step);
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 6,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h4" fontWeight="500" gutterBottom>
          {items[activeStep].name}
        </Typography>
        <Typography variant="body2" color="text.secondary" className="welcome__description">
          {items[activeStep].description}
        </Typography>
        <AutoPlaySwipeableViews
          axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
          index={activeStep}
          onChangeIndex={handleStepChange}
          enableMouseEvents
        >
          {items.map((step, index) => (
            <div key={step.name}>
              {Math.abs(activeStep - index) <= 2 ? (
                <Box
                  component="img"
                  sx={{
                    minHeight: 300,
                    display: 'block',
                    maxWidth: 375,
                    marginTop: 5,
                    marginBottom: 6,
                    overflow: 'hidden',
                    width: '100%',
                  }}
                  src={step.image}
                  alt="a man is doing yoga"
                />
              ) : null}
            </div>
          ))}
        </AutoPlaySwipeableViews>
        <MobileStepper
          steps={maxSteps}
          position="static"
          activeStep={activeStep}
        />
        <Button
          component={Link}
          to="/register"
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
        >
          Присоединиться
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
    </Container>
  );
};

export default SplashScreens;
