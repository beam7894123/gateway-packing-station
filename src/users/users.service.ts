import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { CreateUserDto } from './dto/create-user.dto';
import { hash } from 'argon2';

export type User = {
  id: number;
  username: string;
  password: string;
  hashedRefreshToken: string | null;
};

export type PublicUser = Omit<User, 'password' | 'hashedRefreshToken'>;

@Injectable()
export class UsersService {
  constructor(private readonly prisma: PrismaService) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    const { password, ...user } = createUserDto;
    const hashedPassword = await hash(password);
    return await this.prisma.users.create({
      data: {
        password: hashedPassword,
        ...user,
      },
    });
  }

  async findByUsername(username: string): Promise<User | undefined> {
    const user = await this.prisma.users.findUnique({
      where: {
        username,
      },
    });
    if (!user) {
      return undefined;
    }
    return {
      id: user.id,
      username: user.username,
      password: user.password,
      hashedRefreshToken: user.hashedRefreshToken,
    };
  }

  async findByEmail(email: string): Promise<User | undefined> {
    const user = await this.prisma.users.findUnique({
      where: {
        email,
      },
    });
    if (!user) {
      return undefined;
    }
    return {
      id: user.id,
      username: user.username,
      password: user.password,
      hashedRefreshToken: user.hashedRefreshToken,
    };
  }

  async findByUsernameField(username: string): Promise<User | undefined> {
    const user = await this.prisma.users.findFirst({
      where: {
        OR: [
          {
            username,
          },
          {
            email: username,
          },
        ],
      },
    });
    if (!user) {
      return undefined;
    }
    return {
      id: user.id,
      username: user.username,
      password: user.password,
      hashedRefreshToken: user.hashedRefreshToken,
    };
  }
}
