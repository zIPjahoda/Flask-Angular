import { Routes } from '@angular/router';
import { HomeComponent } from './components/home';
import { AboutComponent } from './about';
import { NoContentComponent } from './no-content';

import { LoginFormComponent } from './components/login';
import { RegisterFormComponent} from './components/register';
import { NotFoundComponent } from './shared/utils';
import { DataResolver } from './app.resolver';

export const ROUTES: Routes = [
  {
    path: '',
    redirectTo: '/login',
    pathMatch: 'full'
  },
  { path: 'register', component: RegisterFormComponent },
  // { path: 'sessionexpired', component: SessionExpiredComponent },
  // { path: 'forgot-password', component: ErrorMessage },
  { path: 'login', component: LoginFormComponent },
  { path: 'home', component: HomeComponent },
  { path: '**', component: NotFoundComponent }
];
