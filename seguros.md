AuthService.js

import 'whatwg-fetch';

class AuthService {

  constructor(postUrl) {
    this.postUrl = postUrl;
  }

  login = (username, password) => {
    const details = {
      userName: username,
      password,
      grant_type: 'password'
    };
    let formBody = [];
    Object.keys(details).forEach((property) => {
      const encodedKey = encodeURIComponent(property);
      const encodedValue = encodeURIComponent(details[property]);
      formBody.push(`${encodedKey}=${encodedValue}`);
    });

    formBody = formBody.join('&');
    const loginUrl = this.postUrl;
    return new Promise((resolve, reject) => {
      fetch(loginUrl, {
        credentials: 'include',
        method: 'POST',
        headers: {
          Accept: '*/*',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formBody
      })
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        if (json.error) {
          reject(json.error_description);
        } else {
          localStorage.setItem('query-execute:token', json.access_token);
          resolve(true);
        }
      })
      .catch((error) => {
        reject(error);
      });
    });
  }

  logout = () => {
    const key = 'query-execute:token';
    return new Promise((resolve, reject) => {
      if (!this.removeExistingItem(key)) {
        reject('No existe');
      }
      this.removeExistingItem(key);
      const cookies = new Cookies();
      cookies.remove('JwtToken');
      resolve(true);
    });
  }

  removeExistingItem = (key) => {
    if (localStorage.getItem(key) === null) {
      return false;
    }
    localStorage.removeItem(key);
    return true;
  };
}

export default AuthService;


AuthStore
import { observable/*,runInAction*/ } from 'mobx';

class AuthStore {
  username;
  password;
  @observable error;
  loginResult;
  logoutResult

  constructor(authService, snackBarStore, credentials) {
    this.authService = authService;
    this.snackBarStore = snackBarStore;
    this.username = credentials.username;
    this.password = credentials.password;
    this.error = '';
    this.loginResult = false;
    this.logoutResult = false;
  }

  login = () => {
    return new Promise((resolve, reject) => {
      this.authService.login(this.username, this.password).then((result) => {
        this.loginResult = result;
        resolve(result);
      }).catch((error) => {
        reject(error);
      });
    });
  }

  logout = (key) => {
    return new Promise((resolve, reject) => {
      this.authService.logout(key).then((result) => {
        this.logoutResult = result;
        resolve(true);
      }).catch(() => {
        reject('Hubo un error en el LoginStore');
      });
    });
  }
}

export default AuthStore;

type.js
export const POST_LOGIN_PENDING = 'POST_LOGIN_PENDING';
export const POST_LOGIN_FULFILLED = 'POST_LOGIN_FULFILLED';
export const POST_LOGIN_REJECTED = 'POST_LOGIN_REJECTED';
export const PATCH_LOGIN_ERROR = 'PATCH_LOGIN_ERROR';

useservice.js
export const loginUserAPI = createAsyncAction(
    'POST_LOGIN',
    async (bodyReq) => {
        const headers = { 'Content-Type': 'application/json' };
        const body = JSON.stringify(bodyReq);
        const res = await fetch(`${authUrlApi}/login`, { method: 'POST', headers, body })
        .then((response) => validateResponse(response))
        .catch((error) => {
            throw exceptionCodeResponse(error);
        });
        return res;
    }
);

export const getDataUserLoggedIn = () => {
    const obj = JSON.parse(localStorage.getItem('persist:root_cotizador_backoffice'))
    const auth = JSON.parse(obj.auth)
    const userData = jwt_decode(auth.token)

    const headers = { Authorization: `Bearer ${auth.token}` };
    const response = axios.get(`${authUrlApi}v1/usersInfo/${userData.user._id}`, { headers })
    return response
}

login.js
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { navigate } from '@reach/router';
import {
    Avatar,
    Button,
    TextField,
    FormControlLabel,
    Checkbox,
    Link,
    Grid,
    Typography
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import { postLogin, patchErrorLogin, setAuthToken } from '../actions/authActions';
import { getDataUserLoggeIn } from '../actions/userInfoActions';
import { useInputValue } from '../hooks/useInputValue';
import LoadingModal from '../components/modal/loadingModal';
import MessageFailure from '../components/messages/messageFailure';
import { authUrlBase } from '../utils/urls';

const useStyles = makeStyles((theme) => ({
    paper: {
        backgroundColor: theme.palette.common.white,
        marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main
    },
    form: {
        width: '100%',
        marginTop: theme.spacing(1)
    },
    submit: {
        margin: theme.spacing(3, 0, 2)
    }
}));

const Login = ({ location }) => {
    const classes = useStyles();
    const dispatch = useDispatch();
    const isAuth = useSelector((state) => state.auth);
    const user = useInputValue('');
    const password = useInputValue('');

    const token = new URLSearchParams(location.search).get('token');

    if (!isAuth.token && token) {
        dispatch(setAuthToken(token));
    }
    useEffect(() => {
        if (isAuth.token) {
            navigate('/dashboard');
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isAuth.token]);

    const handleSubmitUser = (event) => {
        event.preventDefault();
        if (user.value && password.value) {
            const credential = { email: user.value, password: password.value };
            dispatch(postLogin(credential));
        }
    };

    const handleErrorLogin = () => {
        dispatch(patchErrorLogin());
    };

    if (!token) {
        return window.location.assign(`${authUrlBase}login/agent`);
    }

    return (
        <Grid container justify="center" className="appContainer">
            {isAuth.loading && <LoadingModal />}
            {isAuth.error && <MessageFailure close={handleErrorLogin} />}
            <Grid
                item
                xs={12}
                md={4}
                className="cardAppContainer"
                style={{ marginTop: 32 }}
            >
                <Grid
                    container
                    justify="center"
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center'
                    }}
                >
                    <Avatar className={classes.avatar}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
						Login
                    </Typography>
                </Grid>
                <form
                    className={classes.form}
                    onSubmit={(event) => handleSubmitUser(event)}
                >
                    <TextField
                        label="Usuario"
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        autoFocus
                        {...user}
                    />
                    <TextField
                        variant="outlined"
                        margin="normal"
                        label="contraseña"
                        type="password"
                        required
                        fullWidth
                        {...password}
                    />
                    <FormControlLabel
                        control={<Checkbox value="remember" color="primary" />}
                        label="Recordar Usuario"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                    >
						Ingresar
                    </Button>
                    <Grid container>
                        <Grid item xs>
                            <Link href="#" variant="body2">
								Olvido su contraseña?
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </Grid>
        </Grid>
    );
};

export default Login;

**local storage**:

value: persist:root_cotizador_backoffice
key:
auth
: 
"{\"token\":\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY1NjExYTc0NjEyYWYxYzBkZTJmMzE1NyIsImVtYWlsIjoiYXV0b3NAbHV4dXJ5c2VndXJvcy5jb20iLCJwZXJtaXNzaW9ucyI6eyJBZ2VudCI6eyJFbXBsb3llZUNvbmZpZ3VyYXRpb24iOltdLCJDb21taXNzaW9uQmFsYW5jZVdpZGdldCI6W10sIkV4dGVuZGVkUHJvZmlsZSI6W10sIkRhc2hib2FyZCI6WyJyZWFkIl0sIk5vdGlmaWNhdGlvbnMiOlsiY3JlYXRlIiwicmVhZCJdLCJBdHRlbnRpb25Qb2ludHMiOltdLCJQb3J0Zm9saW9RdWVyeSI6W10sIkNvbW1pc3Npb25CYWxhbmNlIjpbXSwiQmxhY2tiZXJyeSI6W10sIkNvbW1pc3Npb25zIjpbXSwiV0ZSZXF1ZXN0cyI6W10sIkF3YXJkcyI6W10sIlNpbmlzdGVyIjpbXSwiUmVmdW5kIjpbXSwiRW1lcmdlbmN5IjpbXSwiQ2hlY2tpbmdBY2NvdW50IjpbXSwiUXVvdGVyIjpbInJlYWQiXSwiUXVvdGVyRmxhc2giOltdLCJRdW90ZXJIREkiOltdLCJOZXdzIjpbInJlYWQiXSwiTGVhZCI6WyJyZWFkIl0sIlByb3Bvc2FsIjpbXSwiU2luaXN0ZXJSZWdpc3RlciI6W10sIlRyYW5zcG9ydENlcnRpZmljYXRlIjpbXSwiUGF5bWVudExpbmtzIjpbXSwiRXhjZWxUZW1wbGF0ZSI6W119fSwidXNlckNvZGUiOiIxLTE4NDU5NCIsImluc3VyZWRDb2RlIjoiIiwicGhvbmUiOiIzMTM4ODM1OTM4IiwicHJvZmlsZVR5cGUiOiJpbnRlcm1lZGlhcnkiLCJicmFuY2hzIjpbIjY0NmY4N2Y2ZWFjZTY3MmM0N2Y3NmQ2NiJdLCJwYXNzd29yZEV4cGlyYXRpb24iOiIyMDI2LTA0LTIzVDE3OjIyOjMxLjQ4MFoifSwiaWF0IjoxNzc2MTg2NTM3LCJleHAiOjE3NzYyNzI5Mzd9.4tqf1Iw0lriBLq5Cnty3vPTBFCtn05Um5a_NLZD_dPQ\",\"loading\":false,\"error\":false}"
_persist
: 
"{\"version\":-1,\"rehydrated\":true}"


value:persist:root_cotizador_client
key:{lead: "{"data":{},"loading":false,"error":false}", _persist: "{"version":-1,"rehydrated":true}"}
lead
: 
"{\"data\":{},\"loading\":false,\"error\":false}"
_persist
: 
"{\"version\":-1,\"rehydrated\":true}"

**cookie**:

domain: thot-sde-auth.sise3g.com.co
value: express:sess
key:eyJzZXNzaW9uSWQiOiI3ODQ2YzEyYy1iNzM2LTQ2MTctYTA3YS04YzdjYTRjMzZiYmUifQ==
expire/max-age:2026-04-15T17:08:56.847Z

domain:thot-sde-auth.sise3g.com.co
value: express:sess.sig
ekm_3fThX4I-S7kfZXFlocCiEPo

PROMPT PARA CURSOR:

Necesito que analices el código actual del bot de Selenium en Python y propongas un plan de mejora antes de escribir cualquier código.
Contexto del problema:
Tenemos un bot en Python con Selenium que automatiza login en la página SegurosEstado. Cuando el bot falla o se cierra bruscamente, la sesión queda activa en el servidor (usa Socket.io internamente), lo que bloquea el acceso manual posterior con el mensaje de "5 sesiones activas". El logout de esta página es únicamente del lado del frontend: no hace ninguna llamada al backend, solo limpia el localStorage y redirige al login.
Lo que ya existe:

El bot ya tiene algún manejo de errores, respétalo y adáptate a su estructura actual sin reescribirlo desde cero.

Lo que está faltando y debe agregarse:

Antes de cerrar el navegador en cualquier escenario (éxito, error o cierre forzado), se debe ejecutar una limpieza del localStorage desde Selenium usando JavaScript, específicamente la clave persist:root_cotizador_backoffice.
Luego de limpiar el localStorage, se debe localizar el botón de cerrar sesión en la página y hacer clic en él para que el Socket.io se desconecte limpiamente del servidor.
Solo después de esos dos pasos se debe llamar a driver.quit().
Esta rutina de limpieza debe ejecutarse también si el proceso recibe señales del sistema operativo como SIGTERM o SIGINT (Ctrl+C o kill externo).

Instrucciones para Cursor:

Primero lee todo el código existente del bot.
Antes de escribir una sola línea de código, hazme las preguntas que necesites: cómo está estructurado el try/except actual, dónde está el driver, cómo se llama el botón de logout en el HTML (selector CSS, XPath o ID), y cualquier otra duda que tengas.
Luego presenta un plan paso a paso de los cambios que vas a hacer, indicando exactamente qué archivos y funciones vas a modificar.
Espera mi aprobación del plan antes de proceder a escribir código.
Cuando escribas código, adáptate al estilo y estructura que ya existe, no lo reescribas desde cero.