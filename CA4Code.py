class Commit(object):


    def __init__(self, revision, author, date, time, number_of_lines, changed_path=[], comment=[]):
        self.revision = revision
        self.author = author
        self.date = date
        self.time = time
        self.number_of_lines = number_of_lines
        self.changed_path = changed_path
        self.comment = comment





    def __repr__(self):
        return self.revision + ',' + self.author + \
               ',' + self.date + ',' + self.time + ',' + str(self.number_of_lines) + \
               ',' + ' '.join(self.comment) + '\n'


def get_commits(data):
    sep = 72 * '-'
    commits = []
    index = 0


    while index < len(data):
        try:
            # parse each of the commits and put them into a list of commits
            details = data[index + 1].split('|')
            # the author with spaces at end removed.
            commit = Commit(details[0].strip(),
                            details[1].strip(),
                            details[2].strip().split(' ')[0],
                            details[2].strip().split(' ')[1],
                            int(details[3].strip().split(' ')[0]))
            change_file_end_index = data.index('', index + 1)
            commit.changed_path = data[index + 3: change_file_end_index]

            #Break out the Additions, Modifications and deletions by taking the first letter of each line of "Changed_Path" and
            # putting them into seperate buckets.
            commit.add_paths = filter(lambda x:x == 'A', (line.split()[0] for line in commit.changed_path))
            commit.mod_paths = filter(lambda x:x == 'M', (line.split()[0] for line in commit.changed_path))
            commit.del_paths = filter(lambda x:x == 'D', (line.split()[0] for line in commit.changed_path))



            commit.comment = data[change_file_end_index + 1:
            change_file_end_index + 1 + commit.number_of_lines]
            # add details to the list of commits.
            commits.append(commit)
            index = data.index(sep, index + 1)
        except IndexError:
            index = len(data)
    return commits


def read_file(any_file):
    # use strip to strip out spaces and trim the line.
    return [line.strip() for line in open(any_file, 'r')]


def save_commits(commits, any_file):
    my_file = open(any_file, 'w')
    my_file.write("revision,author,date,time,number_of_lines,comment\n")
    for commit in commits:
        my_file.write(str(commit))
    my_file.close()


if __name__ == '__main__':
    # open the file - and read all of the lines.
    changes_file = 'testfile.txt'
    data = read_file(changes_file)
    print len(data)
    commits = get_commits(data)
    print len(commits)
    print commits[0]
    print commits[0].author
    #total the additions, deletions and modifications made on the system
    totaladd = (reduce(lambda x,y : x + y, (len(commit.add_paths) for commit in commits)))
    totaldel = (reduce(lambda x,y : x + y, (len(commit.del_paths) for commit in commits)))
    totalmod = (reduce(lambda x,y : x + y, (len(commit.mod_paths) for commit in commits)))
    #total all changes
    totalchanges = totaladd + totaldel + totalmod


    print "Total Changes made on the System : " + str(totalchanges)
    print "Total Additions = " + str(totaladd)
    print "Total Deletions = " + str(totaldel)
    print "Total Modifications = " + str(totalmod)


    save_commits(commits, 'changes.csv')




