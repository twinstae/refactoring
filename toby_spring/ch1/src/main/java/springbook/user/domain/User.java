package springbook.user.domain;

import lombok.Getter;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@RequiredArgsConstructor
public class User {
    @NonNull String id;
    @NonNull String name;
    @NonNull String password;
}
