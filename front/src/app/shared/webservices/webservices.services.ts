import { Component, OnInit, Injectable } from '@angular/core';
import { AuthenticationService } from '../authentication';
import { Router } from '@angular/router';
import { Http, Response } from '@angular/http';

@Injectable()
export class WebService {
  constructor(private authService: AuthenticationService) { }

  public HOME : string = '/api/home/';
  public WALLET: string = '/api/wallet/';

  public getDataFromBackend() {
    return this.authService.getResource(this.HOME + 'protected');
  }

  public getCoinsFromBackend(){
    return this.authService.getResource(this.HOME + 'coins')
  }

  public postAddWallet(body: object){
    return this.authService.postJSON(body,this.WALLET + 'add')
  }


  public isAuthenticated() {
    if (!this.authService.isAuthenticated()) {
      this.authService.clearUserDataAndRedirect();
    }
  }
}
