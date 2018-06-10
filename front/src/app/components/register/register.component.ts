import { Component, Injectable, ViewChild, OnInit } from '@angular/core';
import { FormGroup, Validators, FormControl } from '@angular/forms';
import { AuthenticationService } from '../../shared/authentication/authentication.service';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Rx';

@Component({
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  providers: [AuthenticationService]
})

export class RegisterFormComponent implements OnInit {

  public myform: FormGroup;
  public color: string = 'blue';
  public registerText: string = 'Okej';

  constructor(private _service: AuthenticationService, private router: Router) {
    let group: any = {};
    group.username = new FormControl('', Validators.required);
    group.password = new FormControl('', Validators.required);
    group.email = new FormControl('', Validators.required);
    group.type = new FormControl('register');
    this.myform = new FormGroup(group);
  }

  public ngOnInit(): void {
    console.log('Inside the register page');
  }

  public registerUser() {
    let body = {
      username: this.myform.controls['username'].value,
      password: this.myform.controls['password'].value,
      email: this.myform.controls['email'].value
    };
    this._service.register(body).subscribe((data) => {
      this.router.navigate(['/home']);
    }, (error) => this.handleError(error));
  }

  private handleError(error: any) {
    // In a real world app, we might use a remote logging infrastructure
    // We'd also dig deeper into the error to get a better message
    let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg); // log to console instead
    this.color = 'red';
    this.registerText = errMsg;
    return Observable.throw(errMsg);
  }

}
