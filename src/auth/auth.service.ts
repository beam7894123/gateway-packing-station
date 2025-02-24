import {
  ConflictException,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { PublicUser, User, UsersService } from 'src/users/users.service';
import { verify } from 'argon2';
import { CreateUserDto } from 'src/users/dto/create-user.dto';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
  ) {}

  async registerUser(
    createUserDto: CreateUserDto,
  ): Promise<{ access_token: string }> {
    let user = await this.usersService.findByUsername(createUserDto.username);
    if (user) throw new ConflictException('Username already exists!');
    user = await this.usersService.findByEmail(createUserDto.email);
    if (user) throw new ConflictException('Email already exists!');
    user = await this.usersService.create(createUserDto);

    return this.login(user);
  }

  async validateUser(username: string, password: string): Promise<PublicUser> {
    const user = (await this.usersService.findByUsernameField(
      username,
    )) as User;
    if (user && (await verify(user.password, password))) {
      const result = {
        id: user.id,
        username: user.username,
      } as PublicUser;
      return result;
    }
    throw new UnauthorizedException('Invalid credentials');
  }

  login(user: PublicUser): { access_token: string } {
    const payload = { username: user.username, sub: user.id };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }
}
