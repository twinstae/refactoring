import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import springbook.user.dao.UserDao;
import springbook.user.domain.User;

import java.sql.SQLException;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = "/applicationContext.xml")
public class UserDaoTest {

    @Autowired
    private UserDao dao;
    private User a, b, c;

    @Before
    public void setUp() throws SQLException {
        dao.deleteAll();
        assertCount(dao, 0);

        a = new User("twinsjae", "jaehee kim", "spring1");
        b = new User("twinstae", "taehee kim", "spring2");
        c = new User("jojoldu", "dongwook lee", "spring3");
    }


    private void assertCount(UserDao dao, int i) throws SQLException {
        assertThat(dao.getCount(), is(i));
    }

    @Test
    public void addAndGet() throws SQLException {
        dao.add(a);
        assertCount(dao, 1);
        dao.add(b);

        User getUser = dao.get(a.getId());
        assertThat(getUser.getName(), is(a.getName()));
        assertThat(getUser.getPassword(), is(a.getPassword()));

        User getUserB = dao.get(b.getId());
        assertThat(getUserB.getName(), is(b.getName()));
        assertThat(getUserB.getPassword(), is(b.getPassword()));
    }

    @Test
    public void count() throws SQLException {
        dao.add(a);
        assertCount(dao, 1);
        dao.add(b);
        assertCount(dao, 2);
        dao.add(c);
        assertCount(dao, 3);
    }

    @Test(expected = EmptyResultDataAccessException.class)
    public void getUserFailure() throws SQLException {
        dao.get("unknown");
    }
}
