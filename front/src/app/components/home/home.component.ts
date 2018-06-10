import {Component, OnInit, OnDestroy, AfterViewInit} from '@angular/core';
import { Http, Response } from '@angular/http';
import { AuthenticationService } from '../../shared/authentication';
import { Router } from '@angular/router';
import { NavbarComponent } from '../../shared/navbar';
import { WebService } from '../../shared/webservices';
import {ControlContainer, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: [WebService, AuthenticationService]
})

export class HomeComponent implements OnInit, AfterViewInit, OnDestroy {

  public addressGroup: FormGroup;

  public heroes = [];
  public coins = [];
  constructor(private http: Http, private router: Router, private webservice: WebService) {
    let group: any = {};
    group.token_id = new FormControl('',Validators.required);
    group.address = new FormControl('',Validators.required);
    group.type = new FormControl('wallet');
    this.addressGroup = new FormGroup(group);
  }

  public ngOnInit() {
    this.webservice.isAuthenticated();
    this.getData();
  }

  public ngAfterViewInit(): void {
    this.getCoins();
  }

  public ngOnDestroy() {
    // Will clear when component is destroyed e.g. route is navigated away from.
    console.log('destroyed');
  }

  public add_wallet(){
    let body = {
      token_id: this.addressGroup['token_id'].value,
      address: this.addressGroup['address'].value
    };
    console.log('ook funguje');
    this.webservice.postAddWallet(body);
    //   .subscribe(
    //     (data) => this.handleData(data),
    //     (err) => this.logError(err),
    //     ()=> console.log('got data')
    //
    // );
  }

  public clear() {
    this.heroes = [];
  }


  /**
   * Fetch the data from the python-flask backend
   */
  public getData() {
    this.webservice.getDataFromBackend()
      .subscribe(
      (data) => this.handleData(data),
      (err) => this.logError(err),
      () => console.log('got data')
      );
  }

  public getCoins(){
    this.webservice.getCoinsFromBackend().subscribe(
      (data) => this.handleCoin(data),
      (err) =>this.logError(err),
      ()=> console.log('got data')
    )

  }

  private handleData(data: Response) {
    if (data.status === 200) {
      let receivedData = data.json();
      this.heroes = receivedData['Heroes'];
    }
    console.log(data.json());
  }

  private handleCoin(data: Response){
    console.log(data);
    console.log("dopici tohle============");
    if(data.status === 200){
      let receivedData = data.json();
      this.coins = receivedData['coins'];
      console.log(this.coins);
    }
  }

  private logError(err: Response) {
    console.log('There was an error: ' + err.status);
    if (err.status === 0) {
      console.error('Seems server is down');
    }
    if (err.status === 401) {
      this.router.navigate(['/sessionexpired']);
    }
  }
}
