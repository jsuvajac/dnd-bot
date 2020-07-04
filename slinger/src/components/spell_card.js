import React from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

import { withStyles } from '@material-ui/core';

const styles = {
  root: {
    width: '30',
    height: '45',
  },
  card_text: {
    align: 'left',
    display: 'inline',
    marginBottom: 12,
  }
};

class SpellCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = { flip_back: false };
  }

  flip() {
  }

  render() {
    if (this.state.flip_back) {
      return (
        <Card className={this.props.root}>
          <CardContent>
            <Typography variant="h5" component="h2">
              {this.props.spell['Name']}
            </Typography>

            <Typography paragraph className={this.props.card_text} color="textSecondary">
              {this.props.spell['Text']}
            </Typography>

          </CardContent>

          <CardActions>
            <Button
              size="small"
              onClick={() => { 
                this.setState({flip_back: !this.state.flip_back})
              }}
              >
              Flip
            </Button>
          </CardActions>

        </Card>
      )
    } else {

      return (
        <Card className={this.props.root}>
          <CardContent>
            <Typography variant="h5" component="h2">
              {this.props.spell['Name']}
            </Typography>

            <Typography className={this.props.card_text} color="textSecondary">
              {'Level: ' + this.props.spell['Level']}
            </Typography>
            <Typography className={this.props.card_text} color="textSecondary">
              {'Range: ' + this.props.spell['Range']}
            </Typography>
            <Typography className={this.props.card_text} color="textSecondary">
              {'Components: ' + this.props.spell['Components']}
            </Typography>
            <Typography className={this.props.card_text} color="textSecondary">
              {'Duration: ' + this.props.spell['Duration']}
            </Typography>
            <Typography className={this.props.card_text} color="textSecondary">
              {'Source: ' + this.props.spell['Page']}
            </Typography>
            <Typography className={this.props.card_text} color="textSecondary">
              {'this.props: (' + this.props.spell['Class'].slice(-1) + ')'}
            </Typography>
            <Typography className={this.props.card_text} color="textSecondary">
              {'Casting time:' + this.props.spell['Casting time']}
            </Typography>

          </CardContent>

          <CardActions>
            <Button
              size="small"
              onClick={() => { 
                this.setState({flip_back: !this.state.flip_back})
              }}
              >
              Flip
            </Button>
          </CardActions>

        </Card>
      );

    }
  }
}

export default withStyles(styles)(SpellCard);